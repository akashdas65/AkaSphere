from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        message_id: str,
    ) -> Message | None:

        statement = select(Message).where(
            Message.id == message_id
        )

        return self.db.scalar(statement)

    def get_channel_messages(
        self,
        channel_id: str,
        limit: int = 50,
    ) -> list[Message]:

        statement = (
            select(Message)
            .where(
                Message.channel_id == channel_id,
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(limit)
        )

        messages = list(
            self.db.scalars(statement).all()
        )

        messages.reverse()

        return messages

    def create(
        self,
        channel_id: str,
        user_id: str,
        content: str,
    ) -> Message:

        message = Message(
            channel_id=channel_id,
            user_id=user_id,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def update(
        self,
        message: Message,
        content: str,
    ) -> Message:

        message.content = content
        message.is_edited = True

        self.db.commit()
        self.db.refresh(message)

        return message

    def delete(
        self,
        message: Message,
    ) -> None:

        self.db.delete(message)
        self.db.commit()