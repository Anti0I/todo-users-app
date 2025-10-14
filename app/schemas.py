from pydantic import BaseModel, Field
from datetime import date, datetime
from .models import StatusEnum, PriorityEnum

class TaskModel(BaseModel):
    task_id: int = None
    task_name: str = Field(..., min_length=1)
    user_id: int
    created_at: datetime = None
    status: StatusEnum = StatusEnum.pending
    due_date: date = None
    priority: PriorityEnum = PriorityEnum.medium

    class Config:
        orm_mode = True
