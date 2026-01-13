from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from scheduler.db.database import Base
from passlib.hash import bcrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="user")
    task_runs = relationship("TaskRun", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)
