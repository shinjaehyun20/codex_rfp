from apps.worker.worker.celery_app import celery_app
from apps.api.app.db.session import SessionLocal
from apps.api.app.services.orchestrator import run_production_pipeline

@celery_app.task(name="worker.run_pipeline")
def run_pipeline_task(run_id: str):
    db = SessionLocal()
    try:
        run_production_pipeline(db, run_id)
    finally:
        db.close()
