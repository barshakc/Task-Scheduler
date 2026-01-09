from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from models.enums import ScheduleType, TaskStatus

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

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
