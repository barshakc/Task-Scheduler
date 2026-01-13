from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from scheduler.db.database import get_db
from scheduler.models.task_model import Task as TaskModel
from scheduler.schemas.tasks import TaskCreate, TaskUpdate, Task
from scheduler.models.enums import TaskStatus
from scheduler.api.auth_utils import get_current_user
from scheduler.models.user_model import User
from scheduler.tasks.worker_tasks import run_task

router = APIRouter(tags=["Tasks"])

@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = TaskModel(
        name=task.name,
        description=task.description,
        schedule_type=task.schedule_type,
        schedule_value=task.schedule_value,
        max_retries=task.max_retries,
        retry_delay=task.retry_delay,
        payload=task.payload,
        status=TaskStatus.active,
        user_id=current_user.id  
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(TaskModel).filter(TaskModel.user_id == current_user.id).all()

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}/pause", response_model=Task)
def pause_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.status = TaskStatus.paused
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}/resume", response_model=Task)
def resume_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.status = TaskStatus.active
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}

from scheduler.tasks.worker_tasks import run_task

@router.post("/tasks/{task_id}/run")
def trigger_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run_task.delay(task.id, task.name)
    return {"detail": f"Task {task.name} is scheduled to run"}
