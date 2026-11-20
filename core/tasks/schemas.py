from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=150,
                       description="Title of the task")
    description: Optional[str] = Field(None, max_length=500,
                                       description="Description of the task")
    is_completed: bool = Field(..., description="State of the task")


class TaskCreateSchema(BaseModel):
    pass


class TaskUpdateSchema(BaseModel):
    pass


class TaskResponseSchema(BaseModel):
    id: int = Field(..., description="Unique identifier of the task")
    created_at: datetime = Field(...,
                                 description="Creation date and time of the task")
    updated_at: datetime = Field(...,
                                 description="Updating date and time of the task")
