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

    def register(
        self,
        data: RegisterRequest,
    ) -> User:

        email = str(data.email).lower()
        username = data.username.lower()

        if self.repository.get_by_email(email):
            raise ValueError(
                "Email is already registered"
            )

        if self.repository.get_by_username(username):
            raise ValueError(
                "Username is already taken"
            )

        hashed_password = hash_password(
            data.password
        )

        return self.repository.create(
            email=email,
            username=username,
            full_name=data.full_name,
            hashed_password=hashed_password,
        )

    def login(
        self,
        email: str,
        password: str,
    ) -> tuple[User, AuthTokens]:

        user = self.repository.get_by_email(
            email.lower()
        )

        if user is None:
            raise ValueError(
                "Invalid email or password"
            )

        if not user.is_active:
            raise ValueError(
                "User account is inactive"
            )

        if user.hashed_password is None:
            raise ValueError(
                "Password login is not configured"
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            subject=user.id
        )

        refresh_token = create_refresh_token(
            subject=user.id
        )

        tokens = AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        return user, tokens