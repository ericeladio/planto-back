from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.config import settings
from app.database import get_db
from app.data import (
    add_user,
    create_reset_token,
    get_reset_token,
    get_user_by_email,
    mark_token_used,
    update_password,
)
from app.dependencies import get_current_user
from app.email_service import send_password_reset_email, send_welcome_email
from app.models import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserOut,
    UserRegister,
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(body: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_email(db, body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    password_hash = get_password_hash(body.password)
    user = add_user(db, body.email, password_hash, body.full_name)

    send_welcome_email(user.email, user.full_name or user.email)

    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(
        access_token=access_token,
        user=UserOut(id=user.id, email=user.email, full_name=user.full_name),
    )


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(
        access_token=access_token,
        user=UserOut(id=user.id, email=user.email, full_name=user.full_name),
    )


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
    )


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, body.email)
    if not user:
        return {"message": "If the email exists, you will receive a reset link"}

    token = create_reset_token(db, body.email)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    send_password_reset_email(body.email, reset_link)

    return {"message": "If the email exists, you will receive a reset link"}


@router.post("/reset-password", response_model=TokenResponse)
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    data = get_reset_token(db, body.token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    email = data.email
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    password_hash = get_password_hash(body.new_password)
    update_password(db, email, password_hash)
    mark_token_used(db, body.token)

    access_token = create_access_token(data={"sub": email})

    return TokenResponse(
        access_token=access_token,
        user=UserOut(id=user.id, email=user.email, full_name=user.full_name),
    )
