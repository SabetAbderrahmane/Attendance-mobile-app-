from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.schemas.auth import AuthenticatedUserResponse, LoginRequest, TokenResponse
from app.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(email: str, password: str, db: Session) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return user


@router.post("/login", response_model=TokenResponse)
def login_json(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(payload.email, payload.password, db)
    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=access_token)


@router.post("/login/oauth", response_model=TokenResponse, include_in_schema=False)
def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=AuthenticatedUserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> AuthenticatedUserResponse:
    return AuthenticatedUserResponse(user=current_user)
