from celery import Celery

from apps.api.app.core.config import settings

celery_app = Celery(
    "proposal_ops",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
