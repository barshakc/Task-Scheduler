from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from scheduler.models.enums import TaskStatus

class TaskRunBase(BaseModel):
    task_id: int
    status: TaskStatus
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    result: Optional[dict]

class TaskRun(TaskRunBase):
    id: int

    class Config:
        orm_mode = True
