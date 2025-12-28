from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum

class ScheduleType(str, Enum):
    once = "once"
    interval = "interval"
    cron = "cron"

class TaskStatus(str, Enum):
    active = "active"
    paused = "paused"


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
