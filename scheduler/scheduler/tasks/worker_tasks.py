from scheduler.celery_app import celery_app
from scheduler.db.database import SessionLocal
from scheduler.models.task_model import Task
from scheduler.models.task_run_model import TaskRun
from scheduler.models.enums import TaskStatus
from sqlalchemy.sql import func
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str, payload: dict = None):
    
    db = SessionLocal()
    try:
        # Check if task is active
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            print(f"Task ID {task_id} not found, skipping execution.")
            return {"error": "Task not found"}

        if task.status != TaskStatus.active:
            print(f"Task ID {task_id} is paused. Skipping execution.")
            return {"detail": "Task is paused, not executed"}

        task_run = TaskRun(
            task_id=task_id,
            status=TaskStatus.active
        )
        db.add(task_run)
        db.commit()
        db.refresh(task_run)

        print(f"Starting task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")

        if payload:
            print(f"Payload: {payload}")
        time.sleep(5)  
        result = {"message": f"Task {task_id} completed successfully."}

        # Update TaskRun
        task_run.status = TaskStatus.active  
        task_run.finished_at = func.now()
        task_run.result = result
        db.commit()
        db.refresh(task_run)

        print(f"Finished task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")
        return result

    except Exception as e:
        db.rollback()
        if 'task_run' in locals():
            task_run.status = TaskStatus.paused 
            db.commit()
        raise e
    finally:
        db.close()