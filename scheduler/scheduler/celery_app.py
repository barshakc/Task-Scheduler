from celery import Celery
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

celery_app = Celery(
    "task_scheduler",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        # Poll DB every 30 seconds for active tasks
        "poll-active-tasks-every-30-seconds": {
            "task": "scheduler.tasks.worker_tasks.poll_active_tasks",
            "schedule": 30.0,
        },
        # Test task every 10 seconds
        "run-test-task-every-10-seconds": {
            "task": "scheduler.tasks.worker_tasks.test_task",
            "schedule": 10.0,
        },
    },
)

from scheduler.tasks import worker_tasks
