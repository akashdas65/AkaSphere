from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.channel import Channel


class ChannelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        channel_id: str,
    ) -> Channel | None:

        statement = select(Channel).where(
            Channel.id == channel_id
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        workspace_id: str,
        slug: str,
    ) -> Channel | None:

        statement = select(Channel).where(
            Channel.workspace_id == workspace_id,
            Channel.slug == slug,
        )

        return self.db.scalar(statement)

    def get_workspace_channels(
        self,
        workspace_id: str,
    ) -> list[Channel]:

        statement = (
            select(Channel)
            .where(
                Channel.workspace_id == workspace_id,
                Channel.is_active.is_(True),
            )
            .order_by(Channel.created_at.asc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        workspace_id: str,
        name: str,
        slug: str,
        description: str | None,
        is_private: bool,
    ) -> Channel:

        channel = Channel(
            workspace_id=workspace_id,
            name=name,
            slug=slug,
            description=description,
            is_private=is_private,
        )

        self.db.add(channel)
        self.db.commit()
        self.db.refresh(channel)

        return channel

    def update(
        self,
        channel: Channel,
        name: str,
        description: str | None,
        is_private: bool,
    ) -> Channel:

        channel.name = name
        channel.description = description
        channel.is_private = is_private

        self.db.commit()
        self.db.refresh(channel)

        return channel

    def delete(
        self,
        channel: Channel,
    ) -> None:

        channel.is_active = False

        self.db.commit()