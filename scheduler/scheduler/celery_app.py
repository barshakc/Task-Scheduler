from celery import Celery
import os

celery_app = Celery(
    "task_scheduler",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_RESULT_BACKEND"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "poll-and-schedule-tasks-every-30-seconds": {
        "task": "scheduler.tasks.scheduler_tasks.poll_and_schedule_tasks",
        "schedule": 30.0,
    },
}

celery_app.conf.beat_schedule_filename = "/app/celerybeat-data/celerybeat-schedule"

import scheduler.tasks.scheduler_tasks
import scheduler.tasks.worker_tasks