from apps.api.app.db.session import SessionLocal
from apps.api.app.models import Case, Run
from apps.api.app.services.orchestrator import run_production_pipeline


def test_orchestrator_progress_reaches_100(client):
    db = SessionLocal()
    try:
        case = Case(case_id="CASE-ABCDEFG1")
        db.add(case)
        run = Run(run_id="RUN-ABCDEFG1", case_id=case.case_id, pipeline="production", status="queued", progress=0, current_step="queued")
        db.add(run)
        db.commit()

        run_production_pipeline(db, run.run_id)
        db.refresh(run)
        assert run.progress == 100
        assert run.status == "completed"
    finally:
        db.close()
