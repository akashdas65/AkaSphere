from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self.db.scalar(statement)

    def get_by_id(self, user_id: str) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def create(
        self,
        email: str,
        username: str,
        full_name: str | None,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def mark_as_verified(self, user: User) -> User:
        user.is_verified = True

        self.db.commit()
        self.db.refresh(user)

        return user

    def update_password(
        self,
        user: User,
        new_password: str,
    ) -> User:
        user.hashed_password = hash_password(
            new_password
        )

        self.db.commit()
        self.db.refresh(user)

        return user