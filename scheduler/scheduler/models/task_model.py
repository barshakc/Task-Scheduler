from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from scheduler.db.database import Base
from scheduler.models.enums import ScheduleType, TaskStatus
from datetime import datetime, timezone


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
    next_run = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")
    task_runs = relationship(
        "TaskRun", back_populates="task", cascade="all, delete-orphan"
    )
