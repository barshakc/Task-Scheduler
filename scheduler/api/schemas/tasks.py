from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from scheduler.models.enums import ScheduleType, TaskStatus


# -----------------------------
# Schema for creating a task
# -----------------------------
class TaskCreate(BaseModel):
    name: str = Field(..., example="Send Welcome Message", description="Unique name of the task")
    description: Optional[str] = Field(None, example="Send a welcome message to new users")
    schedule_type: ScheduleType = Field(..., example="interval", description="How the task should run: manual, interval, or cron")
    schedule_value: str = Field(..., example="60", description="Interval in seconds or cron expression, depending on schedule_type")
    max_retries: Optional[int] = Field(3, description="Number of times to retry if the task fails")
    retry_delay: Optional[int] = Field(60, description="Delay in seconds between retries")
    payload: Optional[Dict] = Field(None, example={"recipient": "+123456789", "message": "Welcome!"}, description="Data the task needs to execute")


# -----------------------------
# Schema for updating a task
# -----------------------------
class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedule_type: Optional[ScheduleType] = None
    schedule_value: Optional[str] = None
    max_retries: Optional[int] = None
    retry_delay: Optional[int] = None
    payload: Optional[Dict] = None


# -----------------------------
# Schema for returning a task
# -----------------------------
class Task(TaskCreate):
    id: int
    status: TaskStatus
    created_at: datetime
    next_run: datetime

    class Config:
        orm_mode = True  # <-- Must have to work with SQLAlchemy models
