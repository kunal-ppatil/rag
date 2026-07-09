from celery import Celery

from rag_enterprise.core.config import get_settings

settings = get_settings()

celery_app = Celery("rag_enterprise", broker=settings.redis_url, backend=settings.redis_url)
