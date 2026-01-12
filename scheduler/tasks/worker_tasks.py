from scheduler.celery_app import celery_app
import time

@celery_app.task
def example_task(name: str):
    time.sleep(5)
    return f"Hello {name}, task finished!"
