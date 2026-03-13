from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    total_users = db.scalar(select(func.count()).select_from(User)) or 0
    should_be_admin = payload.is_admin if total_users > 0 else True

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_active=True,
        is_admin=should_be_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
