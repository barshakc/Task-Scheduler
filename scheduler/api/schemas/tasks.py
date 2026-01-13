from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from scheduler.models.enums import ScheduleType, TaskStatus

class TaskCreate(BaseModel):
    name: str = Field(..., example="daily_report")
    description: Optional[str] = None
    schedule_type: ScheduleType
    schedule_value: str
    max_retries: int = 3
    retry_delay: int = 60
    payload: Optional[Dict] = None

class Task(TaskCreate):
    id: int
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedule_type: Optional[ScheduleType] = None
    schedule_value: Optional[str] = None
    max_retries: Optional[int] = None
    retry_delay: Optional[int] = None
    payload: Optional[Dict] = None
