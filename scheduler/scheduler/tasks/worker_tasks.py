from celery import shared_task
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scheduler.models.task_run_model import TaskRun, TaskStatus
from scheduler.core.config import settings
import smtplib
from email.message import EmailMessage
import json

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(msg)

@shared_task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str, payload: dict, task_run_id: int):
    db = SessionLocal()
    try:
        task_run = db.query(TaskRun).filter(TaskRun.id == task_run_id).one_or_none()
        if not task_run:
            return {"error": "TaskRun not found"}

        try:
            recipient = payload.get("recipient")
            message = payload.get("message", "")
            subject = payload.get("subject", f"Task Reminder: {task_name}")

            if not recipient:
                raise ValueError("Recipient email not provided")

            send_email(to_email=recipient, subject=subject, body=message)

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
