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

class TaskBase(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=200)
    user_id: int
    due_date: date | None = None
    status: StatusEnum = StatusEnum.pending
    priority: PriorityEnum = PriorityEnum.medium

    class Config:
        from_attributes = True

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    task_name: str | None = None
    due_date: date | None = None
    status: StatusEnum | None = None
    priority: PriorityEnum | None = None

class TaskResponse(BaseModel):
    id: int
    task_name: str
    user_id: int
    created_at: datetime
    due_date: date | None
    status: StatusEnum
    priority: PriorityEnum

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    role: str | None = None

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str | None = None
    role: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
