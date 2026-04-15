from datetime import datetime
from pydantic import BaseModel, Field
from app.databases.models import TaskStatus


class TaskBase(BaseModel):
    description: str

class TaskRead(TaskBase):
    status: TaskStatus
    estimated_time: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status:TaskStatus | None = Field(default=None)
    estimated_time: datetime | None = Field(default=None)