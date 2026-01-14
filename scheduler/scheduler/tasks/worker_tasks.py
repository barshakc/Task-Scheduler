from celery import shared_task
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scheduler.models.task_run_model import TaskRun, TaskStatus
from scheduler.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@shared_task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str, payload: dict, task_run_id: int):
    db = SessionLocal()
    try:
        task_run = db.query(TaskRun).filter(TaskRun.id == task_run_id).one_or_none()
        if not task_run:
            return {"error": "TaskRun not found"}

        try:
            # ---- YOUR TASK LOGIC ----
            # Example: send message
            print(f"Running task '{task_name}' with payload: {payload}")

            # Mark finished
            task_run.status = TaskStatus.finished
            task_run.finished_at = datetime.now(timezone.utc)
            db.commit()
            return {"status": "success"}

        except Exception as e:
            db.rollback()
            task_run.status = TaskStatus.failed
            task_run.error = str(e)
            task_run.finished_at = datetime.now(timezone.utc)
            db.commit()
            raise

    finally:
        db.close()
