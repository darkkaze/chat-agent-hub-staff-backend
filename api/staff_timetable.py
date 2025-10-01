from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models.auth import Token
from models.staff_models import Staff
from .schemas.staff_schemas import (
    StaffRequest, StaffResponse, StaffListResponse, MessageResponse
)
from helpers.auth import get_auth_token, require_user_or_agent
from datetime import datetime, timezone

router = APIRouter(prefix="/staff", tags=["staff_timetable"])


@router.get("/", response_model=StaffListResponse)
async def list_staff(
    is_active: bool = None,
    token: Token = Depends(get_auth_token),
    db_session: Session = Depends(get_session)
):
    """List all staff members. Optionally filter by active status."""
    await require_user_or_agent(token, db_session)

    statement = select(Staff).order_by(Staff.name)

    # Apply active filter if provided
    if is_active is not None:
        statement = statement.where(Staff.is_active == is_active)

    staff_members = db_session.exec(statement).all()

    staff_responses = [
        StaffResponse(
            id=staff.id,
            name=staff.name,
            schedule=staff.schedule,
            is_active=staff.is_active,
            created_at=staff.created_at,
            updated_at=staff.updated_at
        )
        for staff in staff_members
    ]

    return StaffListResponse(staff=staff_responses)


@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(
    staff_data: StaffRequest,
    token: Token = Depends(get_auth_token),
    db_session: Session = Depends(get_session)
):
    """Create new staff member."""
    await require_user_or_agent(token, db_session)

    new_staff = Staff(
        name=staff_data.name,
        schedule=staff_data.schedule or "{}",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db_session.add(new_staff)
    db_session.commit()
    db_session.refresh(new_staff)

    return StaffResponse(
        id=new_staff.id,
        name=new_staff.name,
        schedule=new_staff.schedule,
        is_active=new_staff.is_active,
        created_at=new_staff.created_at,
        updated_at=new_staff.updated_at
    )


@router.get("/{staff_id}", response_model=StaffResponse)
async def get_staff(
    staff_id: str,
    token: Token = Depends(get_auth_token),
    db_session: Session = Depends(get_session)
):
    """Get specific staff member by ID."""
    await require_user_or_agent(token, db_session)

    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )

    return StaffResponse(
        id=staff.id,
        name=staff.name,
        schedule=staff.schedule,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at
    )


@router.put("/{staff_id}", response_model=StaffResponse)
async def update_staff(
    staff_id: str,
    staff_data: StaffRequest,
    token: Token = Depends(get_auth_token),
    db_session: Session = Depends(get_session)
):
    """Update staff member name and/or schedule."""
    await require_user_or_agent(token, db_session)

    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )

    # Update staff data
    staff.name = staff_data.name
    staff.schedule = staff_data.schedule or "{}"
    staff.updated_at = datetime.now(timezone.utc)

    db_session.add(staff)
    db_session.commit()
    db_session.refresh(staff)

    return StaffResponse(
        id=staff.id,
        name=staff.name,
        schedule=staff.schedule,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at
    )


@router.delete("/{staff_id}", response_model=MessageResponse)
async def delete_staff(
    staff_id: str,
    token: Token = Depends(get_auth_token),
    db_session: Session = Depends(get_session)
):
    """Soft delete staff member by setting is_active=False."""
    await require_user_or_agent(token, db_session)

    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )

    staff.is_active = False
    staff.updated_at = datetime.now(timezone.utc)

    db_session.add(staff)
    db_session.commit()

    return MessageResponse(message=f"Staff member {staff.name} deactivated successfully")
