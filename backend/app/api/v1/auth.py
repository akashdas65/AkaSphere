from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.core.redis import get_redis
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AuthTokens,
    ForgotPasswordRequest,
    LoginRequest,
    OTPRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UserResponse,
    VerifyOTPRequest,
)
from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.services.token_service import TokenService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    service = AuthService(db)

    try:
        user = service.register(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=AuthTokens,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> AuthTokens:
    service = AuthService(db)

    try:
        user, tokens = service.login(
            email=str(data.email).lower(),
            password=data.password,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    token_service = TokenService(redis_client)

    token_service.store_refresh_token(
        user_id=str(user.id),
        refresh_token=tokens.refresh_token,
    )

    return tokens


@router.post(
    "/refresh",
    response_model=AuthTokens,
)
def refresh(
    data: RefreshTokenRequest,
    redis_client=Depends(get_redis),
) -> AuthTokens:
    token_service = TokenService(redis_client)

    try:
        return token_service.rotate_refresh_token(
            data.refresh_token
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    data: RefreshTokenRequest,
    redis_client=Depends(get_redis),
) -> None:
    TokenService(
        redis_client
    ).revoke_refresh_token(
        data.refresh_token
    )

    return None


@router.post(
    "/send-otp",
)
def send_otp(
    data: OTPRequest,
    redis_client=Depends(get_redis),
) -> dict:
    otp_service = OTPService(redis_client)

    otp = otp_service.create_otp(
        str(data.email).lower()
    )

    return {
        "message": "OTP generated successfully",
        "otp": otp,
        "expires_in": OTPService.OTP_EXPIRE_SECONDS,
    }


@router.post(
    "/verify-otp",
)
def verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> dict:
    otp_service = OTPService(redis_client)

    email = str(data.email).lower()

    if not otp_service.verify_otp(
        email=email,
        otp=data.otp,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    repository.mark_as_verified(user)

    return {
        "message": "Email verified successfully",
        "email": user.email,
        "is_verified": user.is_verified,
    }


@router.post(
    "/forgot-password",
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> dict:
    repository = UserRepository(db)

    email = str(data.email).lower()

    user = repository.get_by_email(email)

    # Same response whether the email exists or not.
    # This prevents user enumeration.
    if user is not None:
        otp_service = OTPService(redis_client)

        otp = otp_service.create_otp(email)

        # Development only.
        print(
            f"Password reset OTP for {email}: {otp}"
        )

    return {
        "message": (
            "If the email exists, "
            "a password reset OTP has been sent."
        )
    }


@router.post(
    "/reset-password",
)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> dict:
    otp_service = OTPService(redis_client)

    email = str(data.email).lower()

    if not otp_service.verify_otp(
        email=email,
        otp=data.otp,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password reset request",
        )

    repository.update_password(
        user=user,
        new_password=data.new_password,
    )

    return {
        "message": "Password reset successfully",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> UserResponse:
    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)