from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scheduler.db.database import Base
from scheduler.models.task_run_model import TaskRun, TaskStatus
from scheduler.models.task_model import Task
from scheduler.core.config import settings
import sqlalchemy as sa

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@shared_task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str, payload: dict):
    db: Session = SessionLocal()
    try:
        task_run = TaskRun(
            task_id=task_id,
            status=TaskStatus.active
        )
        db.add(task_run)
        db.commit()
        db.refresh(task_run)

        print(f"Starting task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")
        print(f"Payload: {payload}")

        result = {"message": f"Task {task_id} completed successfully."}
    
        task_run.status = TaskStatus.finished  
        task_run.result = result
        task_run.finished_at = sa.func.now()
        db.commit()

        print(f"Finished task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")

    except Exception as e:
    
        db.rollback()
        if 'task_run' in locals():
            task_run.status = TaskStatus.failed  
            task_run.result = {"error": str(e)}
            db.commit()
        raise e
    finally:
        db.close()
