from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from scheduler.db.database import Base
from scheduler.models.enums import ScheduleType, TaskStatus

class TaskRun(Base):
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    celery_task_id = Column(String, index=True, nullable=True)

    status = Column(Enum(TaskStatus), nullable=False)
    error = Column(String, nullable=True)

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    task = relationship("Task", back_populates="runs")
    user = relationship("User", back_populates="task_runs")