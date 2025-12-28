from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.tasks import TaskCreate, Task, TaskStatus

router = APIRouter(tags=["Tasks"])

tasks: List[Task] = []
task_id_counter = 1

@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    
    new_task = Task(
        id=task_id_counter,
        name=task.name,
        description=task.description,
        schedule_type=task.schedule_type,
        schedule_value=task.schedule_value,
        max_retries=task.max_retries,
        retry_delay=task.retry_delay,
        payload=task.payload,
        status=TaskStatus.active,
        created_at=datetime.utcnow()
    )
    
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@router.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}/pause", response_model=Task)
def pause_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.status = TaskStatus.paused
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}/resume", response_model=Task)
def resume_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.status = TaskStatus.active
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


