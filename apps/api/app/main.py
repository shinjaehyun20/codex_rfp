import hashlib
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from apps.api.app.db.base import Base
from apps.api.app.db.session import engine, get_db
from apps.api.app.models import Artifact, Case, Run, State
from apps.api.app.schemas.api import (
    CaseCreateRequest,
    CaseCreateResponse,
    CaseDetailResponse,
    CasesListResponse,
    HealthResponse,
    RunCreateRequest,
    RunCreateResponse,
    RunStatusResponse,
    RunsListResponse,
)
from apps.api.app.services.ids import make_id
from apps.api.app.services.storage import Storage
from apps.worker.worker.tasks import run_pipeline_task

app = FastAPI(title="proposal-ops api")
Base.metadata.create_all(bind=engine)


def get_storage() -> Storage:
    return Storage()


def _create_artifacts(case_id: str, files: List[UploadFile], db: Session, storage: Storage) -> List[str]:
    artifact_ids: List[str] = []
    for upload in files:
        content = upload.file.read()
        if not content:
            continue
        sha = hashlib.sha256(content).hexdigest()
        artifact_id = make_id("ART")
        suffix = Path(upload.filename or "uploaded.bin").suffix
        key = f"cases/{case_id}/{artifact_id}{suffix}"
        uri = storage.put_bytes(key=key, body=content, content_type=upload.content_type or "application/octet-stream")

        db.add(
            Artifact(
                artifact_id=artifact_id,
                case_id=case_id,
                filename=upload.filename or f"{artifact_id}{suffix}",
                uri=uri,
                sha256=sha,
                type="artifact.v1",
                role="input_document",
                mime=upload.content_type or "application/octet-stream",
            )
        )
        artifact_ids.append(artifact_id)
    return artifact_ids


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", schema_version="v1.0.0", db="OK", storage="OK", worker="OK")


@app.get("/cases", response_model=CasesListResponse)
def list_cases(
    q: Optional[str] = Query(default=None),
    has_learning: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
):
    del has_learning
    stmt = select(Case)
    if q:
        stmt = stmt.where(Case.case_id.like(f"%{q}%"))
    case_rows = db.execute(stmt.order_by(desc(Case.created_at))).scalars().all()

    items = []
    for case in case_rows:
        doc_count = db.execute(select(func.count(Artifact.artifact_id)).where(Artifact.case_id == case.case_id)).scalar_one()
        last_run = db.execute(
            select(Run).where(Run.case_id == case.case_id).order_by(desc(Run.created_at)).limit(1)
        ).scalar_one_or_none()
        items.append(
            {
                "case_id": case.case_id,
                "documents": int(doc_count),
                "last_run_status": last_run.status if last_run else None,
                "bid_status": case.bid_status,
                "created_at": case.created_at.isoformat(),
            }
        )

    return CasesListResponse(items=items)


@app.post("/cases", response_model=CaseCreateResponse)
def create_case(
    payload: CaseCreateRequest = Depends(),
    files: Optional[List[UploadFile]] = File(default=None),
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    case_id = make_id("CASE")
    db.add(Case(case_id=case_id, bid_status=payload.bid_status, bid_score=str(payload.bid_score) if payload.bid_score else None))

    artifact_ids = _create_artifacts(case_id=case_id, files=files or [], db=db, storage=storage)
    db.commit()
    return CaseCreateResponse(case_id=case_id, artifact_ids=artifact_ids)


@app.get("/cases/{case_id}", response_model=CaseDetailResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")

    artifacts = db.execute(select(Artifact).where(Artifact.case_id == case_id).order_by(desc(Artifact.created_at))).scalars().all()
    runs = db.execute(select(Run).where(Run.case_id == case_id).order_by(desc(Run.created_at)).limit(5)).scalars().all()

    return CaseDetailResponse(
        case_id=case.case_id,
        bid_status=case.bid_status,
        bid_score=case.bid_score,
        artifacts=[
            {
                "artifact_id": a.artifact_id,
                "filename": a.filename,
                "uri": a.uri,
                "type": a.type,
                "role": a.role,
                "uploaded": a.created_at.isoformat(),
            }
            for a in artifacts
        ],
        recent_runs=[
            {
                "run_id": r.run_id,
                "pipeline": r.pipeline,
                "status": r.status,
                "progress": r.progress,
                "created_at": r.created_at.isoformat(),
            }
            for r in runs
        ],
    )


@app.post("/cases/{case_id}/artifacts", response_model=CaseCreateResponse)
def upload_artifacts_to_case(
    case_id: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")

    artifact_ids = _create_artifacts(case_id=case_id, files=files, db=db, storage=storage)
    db.commit()
    return CaseCreateResponse(case_id=case_id, artifact_ids=artifact_ids)


@app.get("/runs", response_model=RunsListResponse)
def list_runs(
    limit: int = Query(default=20, ge=1, le=200),
    pipeline: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Run)
    if pipeline:
        stmt = stmt.where(Run.pipeline == pipeline)
    if status:
        stmt = stmt.where(Run.status == status)
    rows = db.execute(stmt.order_by(desc(Run.created_at)).limit(limit)).scalars().all()

    return RunsListResponse(
        items=[
            {
                "run_id": r.run_id,
                "case_id": r.case_id,
                "pipeline": r.pipeline,
                "status": r.status,
                "progress": r.progress,
                "current_step": r.current_step,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ]
    )


@app.post("/runs", response_model=RunCreateResponse)
def create_run(payload: RunCreateRequest, db: Session = Depends(get_db)):
    if not db.get(Case, payload.case_id):
        raise HTTPException(status_code=404, detail="case not found")

    run_id = make_id("RUN")
    db.add(
        Run(
            run_id=run_id,
            case_id=payload.case_id,
            pipeline=payload.pipeline,
            status="queued",
            progress=0,
            current_step="queued",
        )
    )
    db.commit()

    run_pipeline_task.delay(run_id)
    return RunCreateResponse(run_id=run_id)


@app.get("/runs/{run_id}", response_model=RunStatusResponse)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")

    artifacts = db.execute(select(Artifact).where(Artifact.case_id == run.case_id)).scalars().all()
    states = db.execute(select(State).where(State.case_id == run.case_id)).scalars().all()

    return RunStatusResponse(
        run_id=run.run_id,
        case_id=run.case_id,
        pipeline=run.pipeline,
        status=run.status,
        progress=run.progress,
        current_step=run.current_step,
        artifacts=[
            {"artifact_id": a.artifact_id, "filename": a.filename, "uri": a.uri, "type": a.type, "role": a.role}
            for a in artifacts
        ],
        state_refs=[{"state_id": s.state_id, "uri": s.uri, "type": s.type} for s in states],
        errors=[],
    )
