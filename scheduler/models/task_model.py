from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from db.database import Base

class ScheduleType(str, PyEnum):
    once = "once"
    interval = "interval"
    cron = "cron"

class TaskStatus(str, PyEnum):
    active = "active"
    paused = "paused"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    schedule_value = Column(String, nullable=False)
    max_retries = Column(Integer, default=3)
    retry_delay = Column(Integer, default=60)
    payload = Column(JSON, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
