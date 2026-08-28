from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message_reaction import MessageReaction


class MessageReactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        reaction_id: str,
    ) -> MessageReaction | None:

        statement = select(MessageReaction).where(
            MessageReaction.id == reaction_id
        )

        return self.db.scalar(statement)

    def get_user_reaction(
        self,
        message_id: str,
        user_id: str,
        emoji: str,
    ) -> MessageReaction | None:

        statement = select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == user_id,
            MessageReaction.emoji == emoji,
        )

        return self.db.scalar(statement)

    def get_message_reactions(
        self,
        message_id: str,
    ) -> list[MessageReaction]:

        statement = (
            select(MessageReaction)
            .where(
                MessageReaction.message_id == message_id
            )
            .order_by(MessageReaction.created_at.asc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        message_id: str,
        user_id: str,
        emoji: str,
    ) -> MessageReaction:

        reaction = MessageReaction(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji,
        )

        self.db.add(reaction)
        self.db.commit()
        self.db.refresh(reaction)

        return reaction

    def delete(
        self,
        reaction: MessageReaction,
    ) -> None:

        self.db.delete(reaction)
        self.db.commit()