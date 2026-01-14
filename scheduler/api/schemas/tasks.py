from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from scheduler.models.enums import ScheduleType, TaskStatus

class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    schedule_type: ScheduleType
    schedule_value: str
    max_runs: int | None = None   
    next_run: datetime | None = None 
    max_retries: int = 0
    retry_delay: int = 0
    payload: dict


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedule_type: Optional[ScheduleType] = None
    schedule_value: Optional[str] = None
    max_retries: Optional[int] = None
    retry_delay: Optional[int] = None
    max_runs: int | None = None  
    payload: Optional[Dict] = None


class Task(TaskCreate):
    id: int
    status: TaskStatus
    created_at: datetime
    next_run: datetime | None = None

    class Config:
        from_attributes = True
