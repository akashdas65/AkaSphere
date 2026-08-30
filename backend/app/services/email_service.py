from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings


class EmailService:

    @staticmethod
    async def send_otp_email(
        recipient: str,
        otp: str,
        purpose: str = "email verification",
    ) -> None:
        message = EmailMessage()

        message["From"] = (
            f"{settings.email_from_name} "
            f"<{settings.email_from}>"
        )

        message["To"] = recipient

        message["Subject"] = (
            "AkaSphere - Your verification code"
        )

        message.set_content(
            f"""AkaSphere

Your verification code is: {otp}

Purpose: {purpose}

This code will expire in 5 minutes.

If you did not request this code, you can safely ignore this email.

Do not share this code with anyone.

AkaSphere Security
"""
        )

        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            start_tls=True,
            timeout=15,
        )