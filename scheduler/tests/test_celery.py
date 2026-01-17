from scheduler.celery_app import celery_app
from celery.result import AsyncResult

def test_celery_connection():
    try:
        result = AsyncResult("dummy_task_id", app=celery_app)
        assert result is not None
    except Exception:
        assert False, "Celery broker not reachable"
