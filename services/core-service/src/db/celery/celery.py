
from celery import Celery
from app.core.config import settings  # adjust import

celery_app = Celery(
    "worker",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BROKER_URL,  # optional: for result storage
)

celery_app.conf.task_routes = {
    "app.worker.tasks.*": {"queue": "default"},
}
