from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class StaffRequest(BaseModel):
    """Request model for creating/updating staff."""
    name: str
    schedule: Optional[str] = "{}"


class StaffResponse(BaseModel):
    """Response model for staff data."""
    id: str
    name: str
    schedule: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StaffListResponse(BaseModel):
    """Response model for list of staff."""
    staff: List[StaffResponse]


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
