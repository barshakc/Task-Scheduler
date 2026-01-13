from scheduler.celery_app import celery_app
from scheduler.db.database import SessionLocal
from scheduler.models.task_model import Task
from scheduler.models.task_run_model import TaskRun
from scheduler.models.enums import TaskStatus
from sqlalchemy.sql import func
import time

@celery_app.task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str, payload: dict = None):
    db = SessionLocal()
    try:
        task_run = TaskRun(
            task_id=task_id,
            status=TaskStatus.active,
        )
        db.add(task_run)
        db.commit()
        db.refresh(task_run)

        print(f"Starting task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")

        if payload:
            print(f"Payload: {payload}")
        time.sleep(5)  
        result = {"message": f"Task {task_id} completed successfully."}

        task_run.status = TaskStatus.active 
        task_run.finished_at = func.now()
        task_run.result = result
        db.commit()
        db.refresh(task_run)

        print(f"Finished task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})")
        return result

    except Exception as e:
        db.rollback()
        task_run.status = TaskStatus.paused 
        db.commit()
        raise e
    finally:
        db.close()


