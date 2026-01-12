from scheduler.celery_app import celery_app
import time

@celery_app.task(name="scheduler.tasks.worker_tasks.run_task")
def run_task(task_id: int, task_name: str):
    print(f"Starting task {task_name} (ID: {task_id})")
    time.sleep(5)
    print(f"Finished task {task_name} (ID: {task_id})")
    return f"Task {task_id} done"

