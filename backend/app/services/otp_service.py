import secrets
from datetime import timedelta

import redis


class OTPService:
    OTP_LENGTH = 6
    OTP_EXPIRE_SECONDS = 300
    MAX_ATTEMPTS = 5

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def _otp_key(self, email: str) -> str:
        return f"otp:{email.lower()}"

    def _attempt_key(self, email: str) -> str:
        return f"otp_attempts:{email.lower()}"

    def generate_otp(self) -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    def create_otp(self, email: str) -> str:
        email = email.lower()

        otp = self.generate_otp()

        self.redis.setex(
            self._otp_key(email),
            self.OTP_EXPIRE_SECONDS,
            otp,
        )

        self.redis.setex(
            self._attempt_key(email),
            self.OTP_EXPIRE_SECONDS,
            0,
        )

        return otp

    def verify_otp(
        self,
        email: str,
        otp: str,
    ) -> bool:
        email = email.lower()

        attempts = self.redis.get(
            self._attempt_key(email)
        )

        if attempts is not None and int(attempts) >= self.MAX_ATTEMPTS:
            return False

        stored_otp = self.redis.get(
            self._otp_key(email)
        )

        if stored_otp is None:
            return False

        if stored_otp != otp:
            self.redis.incr(
                self._attempt_key(email)
            )
            return False

        self.redis.delete(
            self._otp_key(email)
        )

        self.redis.delete(
            self._attempt_key(email)
        )

        return True