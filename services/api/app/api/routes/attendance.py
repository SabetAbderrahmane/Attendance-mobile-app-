from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.deps import get_db
from app.models.attendance import Attendance
from app.models.event import Event
from app.models.user import User
from app.schemas.attendance import AttendanceRead
from app.schemas.qr import QRCheckInRequest
from app.utils.security import decode_qr_token

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/check-in", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
def check_in_with_qr(
    payload: QRCheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Attendance:
    try:
        token_payload = decode_qr_token(payload.qr_token)
        if token_payload.get("type") != "qr":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid QR token type.",
            )
        event_id = int(token_payload["event_id"])
    except (JWTError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired QR token.",
        )

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    now = datetime.now(UTC).replace(tzinfo=None)
    if now < event.starts_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event check-in has not started yet.",
        )

    if now > event.ends_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event check-in has already ended.",
        )

    existing_record = db.scalar(
        select(Attendance).where(
            Attendance.user_id == current_user.id,
            Attendance.event_id == event_id,
        )
    )
    if existing_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already checked in for this event.",
        )

    record = Attendance(
        user_id=current_user.id,
        event_id=event_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/event/{event_id}", response_model=list[AttendanceRead])
def list_event_attendance(
    event_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Attendance]:
    records = db.scalars(
        select(Attendance).where(Attendance.event_id == event_id)
    ).all()
    return list(records)


@router.get("/me", response_model=list[AttendanceRead])
def list_my_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Attendance]:
    records = db.scalars(
        select(Attendance).where(Attendance.user_id == current_user.id)
    ).all()
    return list(records)
