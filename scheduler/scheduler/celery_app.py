from celery import Celery
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

celery_app = Celery(
    "task_scheduler",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# --- CELERY BEAT SCHEDULE ---
# Poll DB every 30 seconds to schedule tasks
celery_app.conf.beat_schedule = {
    'poll-and-schedule-tasks-every-30-seconds': {
        'task': 'scheduler.tasks.scheduler_tasks.poll_and_schedule_tasks',
        'schedule': 30.0,  # seconds
    },
}

# Autodiscover tasks in scheduler.tasks
import scheduler.tasks.scheduler_tasks
import scheduler.tasks.worker_tasks
