from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime
from sqlalchemy.orm import declarative_base
import datetime
import enum

Base = declarative_base()


class StatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    task_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    due_date = Column(Date, nullable=False)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium)