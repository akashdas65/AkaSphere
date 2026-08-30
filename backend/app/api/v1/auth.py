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
from app.services.email_service import EmailService
from app.services.otp_service import OTPService
from app.services.token_service import TokenService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> UserResponse:

    service = AuthService(db)

    try:
        # Create the user.
        # is_verified remains False until OTP verification.
        user = service.register(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    # Generate OTP and store it in Redis
    otp_service = OTPService(redis_client)

    email = str(user.email).lower()

    otp = otp_service.create_otp(email)

    # Send OTP to the real email address
    try:
        await EmailService.send_otp_email(
            recipient=email,
            otp=otp,
            purpose="email verification",
        )

    except Exception as exc:
        # Remove OTP if email delivery fails.
        redis_client.delete(
            otp_service._otp_key(email)
        )

        redis_client.delete(
            otp_service._attempt_key(email)
        )

        print(
            f"Verification email failed for {email}: {exc}"
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Unable to send verification email. "
                "Please try again later."
            ),
        ) from exc

    return UserResponse.model_validate(user)


# ============================================================
# LOGIN
# ============================================================

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


# ============================================================
# REFRESH TOKEN
# ============================================================

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


# ============================================================
# LOGOUT
# ============================================================

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


# ============================================================
# SEND EMAIL OTP
# ============================================================

@router.post(
    "/send-otp",
)
async def send_otp(
    data: OTPRequest,
    redis_client=Depends(get_redis),
) -> dict:

    email = str(data.email).lower()

    otp_service = OTPService(redis_client)

    # Generate and store OTP in Redis
    otp = otp_service.create_otp(email)

    try:
        # Send OTP to the user's real email
        await EmailService.send_otp_email(
            recipient=email,
            otp=otp,
            purpose="email verification",
        )

    except Exception as exc:
        # If email sending fails, remove the OTP
        # so the user cannot verify with an undelivered code.
        redis_client.delete(
            otp_service._otp_key(email)
        )

        redis_client.delete(
            otp_service._attempt_key(email)
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send verification email. Please try again later.",
        ) from exc

    return {
        "message": "OTP sent successfully",
        "expires_in": OTPService.OTP_EXPIRE_SECONDS,
    }


# ============================================================
# VERIFY EMAIL OTP
# ============================================================

@router.post(
    "/verify-otp",
)
def verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> dict:

    email = str(data.email).lower()

    otp_service = OTPService(redis_client)

    # Verify OTP
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

    # Mark email as verified
    repository.mark_as_verified(user)

    return {
        "message": "Email verified successfully",
        "email": user.email,
        "is_verified": user.is_verified,
    }


# ============================================================
# FORGOT PASSWORD
# ============================================================

@router.post(
    "/forgot-password",
)
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> dict:

    repository = UserRepository(db)

    email = str(data.email).lower()

    user = repository.get_by_email(email)

    # IMPORTANT:
    # Same response is returned whether the account exists
    # or not. This prevents email/user enumeration.

    if user is not None:

        otp_service = OTPService(redis_client)

        otp = otp_service.create_otp(email)

        try:
            await EmailService.send_otp_email(
                recipient=email,
                otp=otp,
                purpose="password reset",
            )

        except Exception:
            # Remove OTP if email delivery fails
            redis_client.delete(
                otp_service._otp_key(email)
            )

            redis_client.delete(
                otp_service._attempt_key(email)
            )

            # Do not reveal whether the account exists
            pass

    return {
        "message": (
            "If the email exists, "
            "a password reset OTP has been sent."
        )
    }


# ============================================================
# RESET PASSWORD
# ============================================================

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

    # Verify password-reset OTP
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

    # Update password
    repository.update_password(
        user=user,
        new_password=data.new_password,
    )

    return {
        "message": "Password reset successfully",
    }


# ============================================================
# CURRENT USER
# ============================================================

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