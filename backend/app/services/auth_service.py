from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthTokens, RegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    # ============================================================
    # REGISTER
    # ============================================================

    def register(
        self,
        data: RegisterRequest,
    ) -> User:

        email = str(data.email).strip().lower()
        username = data.username.strip().lower()

        # --------------------------------------------------------
        # Check duplicate email
        # --------------------------------------------------------

        existing_user = self.repository.get_by_email(email)

        if existing_user:
            raise ValueError(
                "Email is already registered"
            )

        # --------------------------------------------------------
        # Check duplicate username
        # --------------------------------------------------------

        existing_username = (
            self.repository.get_by_username(username)
        )

        if existing_username:
            raise ValueError(
                "Username is already taken"
            )

        # --------------------------------------------------------
        # Hash password using Argon2
        # --------------------------------------------------------

        hashed_password = hash_password(
            data.password
        )

        # --------------------------------------------------------
        # Create user
        #
        # IMPORTANT:
        # is_verified remains False by default.
        #
        # The user MUST verify the OTP before login.
        # --------------------------------------------------------

        user = self.repository.create(
            email=email,
            username=username,
            full_name=data.full_name,
            hashed_password=hashed_password,
        )

        return user

    # ============================================================
    # LOGIN
    # ============================================================

    def login(
        self,
        email: str,
        password: str,
    ) -> tuple[User, AuthTokens]:

        email = email.strip().lower()

        user = self.repository.get_by_email(email)

        # --------------------------------------------------------
        # Do not reveal whether an email exists
        # --------------------------------------------------------

        if user is None:
            raise ValueError(
                "Invalid email or password"
            )

        # --------------------------------------------------------
        # Account status
        # --------------------------------------------------------

        if not user.is_active:
            raise ValueError(
                "User account is inactive"
            )

        # --------------------------------------------------------
        # EMAIL VERIFICATION REQUIRED
        #
        # A user cannot login until their real email
        # address has been verified through OTP.
        # --------------------------------------------------------

        if not user.is_verified:
            raise ValueError(
                "Please verify your email before logging in"
            )

        # --------------------------------------------------------
        # Password must exist
        # --------------------------------------------------------

        if user.hashed_password is None:
            raise ValueError(
                "Password login is not configured"
            )

        # --------------------------------------------------------
        # Verify password
        # --------------------------------------------------------

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        # --------------------------------------------------------
        # Create access token
        # --------------------------------------------------------

        access_token = create_access_token(
            subject=str(user.id)
        )

        # --------------------------------------------------------
        # Create refresh token
        # --------------------------------------------------------

        refresh_token = create_refresh_token(
            subject=str(user.id)
        )

        # --------------------------------------------------------
        # Return authentication tokens
        # --------------------------------------------------------

        tokens = AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        return user, tokens