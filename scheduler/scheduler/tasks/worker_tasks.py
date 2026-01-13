from celery import shared_task
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scheduler.db.database import Base
from scheduler.models.task_run_model import TaskRun, TaskStatus
from scheduler.models.task_model import Task
from scheduler.core.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@shared_task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(*, task_id: int, task_name: str, payload: dict, task_run_id: int):
    """Execute a task and update its TaskRun status in the DB."""
    db = SessionLocal()
    try:
        task_run = db.query(TaskRun).get(task_run_id)
        if not task_run:
            print(f"No active TaskRun found for Task {task_id}")
            return {"message": f"No active TaskRun found for Task {task_id}"}

        print(
            f"Starting task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})"
        )
        print(f"Payload: {payload}")

        result = {"message": f"Task {task_id} completed successfully."}

        task_run.status = TaskStatus.finished
        task_run.result = result
        from sqlalchemy.sql import func

        task_run.finished_at = func.now()
        db.commit()

        print(
            f"Finished task '{task_name}' (Task ID: {task_id}, Run ID: {task_run.id})"
        )
        return result

    except Exception as e:
        db.rollback()
        if task_run:
            task_run.status = TaskStatus.failed
            task_run.result = {"error": str(e)}
            db.commit()
        raise e
    finally:
        db.close()


@shared_task(name="scheduler.tasks.worker_tasks.poll_active_tasks")
def poll_active_tasks():

    db = SessionLocal()
    try:

        active_tasks = db.query(Task).filter(Task.status == TaskStatus.active).all()

        for task in active_tasks:
            try:

                active_run = (
                    db.query(TaskRun)
                    .filter(
                        TaskRun.task_id == task.id, TaskRun.status == TaskStatus.active
                    )
                    .first()
                )
                if active_run:

                    print(
                        f"Skipping task '{task.name}' (Task ID: {task.id}) - already running"
                    )
                    continue

                task_run = TaskRun(
                    task_id=task.id, user_id=task.user_id, status=TaskStatus.active
                )
                db.add(task_run)
                db.commit()
                db.refresh(task_run)

                celery_result = run_task.apply_async(
                    kwargs={
                        "task_id": task.id,
                        "task_name": task.name,
                        "payload": task.payload,
                        "task_run_id": task_run.id,
                    }
                )

                task_run.celery_task_id = celery_result.id
                db.commit()

                print(
                    f"Scheduled task '{task.name}' (Task ID: {task.id}, Run ID: {task_run.id})"
                )

            except Exception as e:
                db.rollback()
                print(
                    f"Failed to schedule task '{task.name}' (Task ID: {task.id}): {e}"
                )

    finally:
        db.close()
