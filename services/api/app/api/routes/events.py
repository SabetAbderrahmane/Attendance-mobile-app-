from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin_user, get_current_user
from app.db.deps import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventRead
from app.schemas.qr import QRTokenResponse
from app.utils.security import create_qr_token

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
) -> Event:
    if payload.ends_at <= payload.starts_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event end time must be after start time.",
        )

    event = Event(
        title=payload.title,
        description=payload.description,
        location=payload.location,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("", response_model=list[EventRead])
def list_events(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Event]:
    events = db.scalars(select(Event).order_by(Event.starts_at.desc())).all()
    return list(events)


@router.get("/{event_id}", response_model=EventRead)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Event:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return event


@router.post("/{event_id}/qr", response_model=QRTokenResponse)
def generate_event_qr(
    event_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
) -> QRTokenResponse:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    qr_token = create_qr_token(event_id=event.id)
    return QRTokenResponse(event_id=event.id, qr_token=qr_token)
