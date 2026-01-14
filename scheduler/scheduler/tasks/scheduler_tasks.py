from celery import shared_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timezone, timedelta

from scheduler.core.config import settings
from scheduler.models.task_model import Task
from scheduler.models.task_run_model import TaskRun, TaskStatus
from scheduler.tasks.worker_tasks import run_task
from sqlalchemy.exc import IntegrityError

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@shared_task(name="scheduler.tasks.scheduler_tasks.poll_and_schedule_tasks")
def poll_and_schedule_tasks():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        active_tasks = (
            db.query(Task)
            .filter(Task.status == TaskStatus.active, Task.next_run <= now)
            .all()
        )

        for task in active_tasks:

            active_run = (
                db.query(TaskRun)
                .filter(TaskRun.task_id == task.id, TaskRun.status == TaskStatus.active)
                .first()
            )
            if active_run:
                continue

            try:

                task_run = TaskRun(
                    task_id=task.id, user_id=task.user_id, status=TaskStatus.active
                )
                db.add(task_run)
                db.commit()
                db.refresh(task_run)

                result = run_task.apply_async(
                    kwargs={
                        "task_id": task.id,
                        "task_name": task.name,
                        "payload": task.payload,
                        "task_run_id": task_run.id,
                    }
                )

                task_run.celery_task_id = result.id
                db.commit()

                if task.schedule_type.name == "interval":
                    task.next_run = now + timedelta(seconds=int(task.schedule_value))
                elif task.schedule_type.name == "cron":
                    task.next_run = task.get_next_cron_run(now)

                db.commit()

            except IntegrityError:
                db.rollback()
            except Exception as e:
                db.rollback()
                print(f"Failed to schedule task {task.id}: {e}")

    finally:
        db.close()
