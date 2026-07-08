from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "stock_analytics"
    broker=settings.celery_broker_url,
    backend=settings.celery_broker_url,
    include=["app.services.analytics"]
    )

celery_app.conf.update(
    task_track_started=True,
    timezone="Europe/Moscow",
    enable_utc=True,
    result_serializer="json",
    task_serializer="json",
    accept_content=["json"]
)