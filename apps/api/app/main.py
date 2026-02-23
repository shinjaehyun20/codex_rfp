import hashlib
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.db.base import Base
from apps.api.app.db.session import engine, get_db
from apps.api.app.models import Artifact, Case, Run, State
from apps.api.app.schemas.api import CaseCreateResponse, RunCreateRequest, RunCreateResponse, RunStatusResponse
from apps.api.app.services.ids import make_id
from apps.api.app.services.storage import Storage
from apps.worker.worker.tasks import run_pipeline_task

app = FastAPI(title="proposal-ops api")
Base.metadata.create_all(bind=engine)


def get_storage() -> Storage:
    return Storage()


@app.post("/cases", response_model=CaseCreateResponse)
def create_case(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
):
    case_id = make_id("CASE")
    db.add(Case(case_id=case_id))

    artifact_ids: List[str] = []
    for upload in files:
        content = upload.file.read()
        sha = hashlib.sha256(content).hexdigest()
        artifact_id = make_id("ART")
        suffix = Path(upload.filename).suffix
        key = f"cases/{case_id}/{artifact_id}{suffix}"
        uri = storage.put_bytes(key=key, body=content, content_type=upload.content_type or "application/octet-stream")

        db.add(
            Artifact(
                artifact_id=artifact_id,
                case_id=case_id,
                uri=uri,
                sha256=sha,
                type="artifact.v1",
                role="input_document",
                mime=upload.content_type or "application/octet-stream",
            )
        )
        artifact_ids.append(artifact_id)

    db.commit()
    return CaseCreateResponse(case_id=case_id, artifact_ids=artifact_ids)


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

    # enqueue (best-effort for local dev)
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
        artifacts=[{"artifact_id": a.artifact_id, "uri": a.uri, "type": a.type, "role": a.role} for a in artifacts],
        state_refs=[{"state_id": s.state_id, "uri": s.uri, "type": s.type} for s in states],
        errors=[],
    )
