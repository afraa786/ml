from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# ============================================================================
# PYDANTIC MODELS (For API validation)
# ============================================================================

class TaskBase(BaseModel):
    """
    Base model with common fields
    Other models will inherit from this
    """
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Literal["low", "medium", "high"] = "medium"


class TaskCreate(TaskBase):
    """
    Model for creating a new task
    Used in POST requests
    """
    pass  # Inherits everything from TaskBase


class TaskUpdate(BaseModel):
    """
    Model for updating a task
    All fields optional (partial update)
    """
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[Literal["low", "medium", "high"]] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Model for returning task data
    Includes database-generated fields
    """
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        # orm_mode allows Pydantic to work with SQLAlchemy models
        # It can read data from objects (not just dicts)
        orm_mode = True
        