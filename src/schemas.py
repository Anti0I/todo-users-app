from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# Task Schemas
class TaskCreate(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=100)
    user_id: int = Field(..., gt=0)
    due_date: date
    status: StatusEnum = StatusEnum.pending
    priority: PriorityEnum = PriorityEnum.medium

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    task_name: str | None = Field(None, min_length=1, max_length=100)
    user_id: int | None = Field(None, gt=0)
    due_date: date | None = None
    status: StatusEnum | None = None
    priority: PriorityEnum | None = None

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id: int
    task_name: str
    user_id: int
    created_at: datetime
    status: StatusEnum
    due_date: date
    priority: PriorityEnum

    class Config:
        from_attributes = True


# User Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    role: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=50)
    role: str | None = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True