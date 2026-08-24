from datetime import timedelta

import redis

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.auth import AuthTokens


class TokenService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def store_refresh_token(
        self,
        user_id: str,
        refresh_token: str,
    ) -> None:
        key = f"refresh_token:{refresh_token}"

        expires_seconds = int(
            timedelta(
                days=7
            ).total_seconds()
        )

        self.redis.setex(
            key,
            expires_seconds,
            user_id,
        )

    def get_user_id_from_refresh_token(
        self,
        refresh_token: str,
    ) -> str | None:
        key = f"refresh_token:{refresh_token}"

        return self.redis.get(key)

    def revoke_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        key = f"refresh_token:{refresh_token}"

        self.redis.delete(key)

    def rotate_refresh_token(
        self,
        refresh_token: str,
    ) -> AuthTokens:

        user_id = self.get_user_id_from_refresh_token(
            refresh_token
        )

        if user_id is None:
            raise ValueError(
                "Invalid or revoked refresh token"
            )

        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise ValueError(
                "Invalid or expired refresh token"
            ) from exc

        if payload.get("type") != "refresh":
            raise ValueError(
                "Refresh token required"
            )

        token_user_id = payload.get("sub")

        if not token_user_id or str(token_user_id) != str(user_id):
            raise ValueError(
                "Invalid refresh token"
            )

        # Revoke old refresh token.
        self.revoke_refresh_token(
            refresh_token
        )

        # Generate new token pair.
        access_token = create_access_token(
            subject=str(user_id)
        )

        new_refresh_token = create_refresh_token(
            subject=str(user_id)
        )

        self.store_refresh_token(
            user_id=str(user_id),
            refresh_token=new_refresh_token,
        )

        return AuthTokens(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )