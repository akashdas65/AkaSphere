from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.message_reaction_repository import (
    MessageReactionRepository,
)
from app.repositories.message_repository import MessageRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.schemas.message_reaction import (
    MessageReactionCreate,
    MessageReactionResponse,
)
from app.services.websocket_manager import connection_manager


router = APIRouter(
    prefix="/messages",
    tags=["Message Reactions"],
)


def check_message_access(
    message_id: str,
    user_id: str,
    db: Session,
):
    message_repository = MessageRepository(db)
    member_repository = WorkspaceMemberRepository(db)

    message = message_repository.get_by_id(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    from app.models.channel import Channel

    channel = db.get(
        Channel,
        message.channel_id,
    )

    if channel is None or not channel.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    membership = member_repository.get_membership(
        channel.workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    return message


@router.post(
    "/{message_id}/reactions",
    response_model=MessageReactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_reaction(
    message_id: str,
    data: MessageReactionCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MessageReactionResponse:

    message = check_message_access(
        message_id,
        user_id,
        db,
    )

    repository = MessageReactionRepository(db)

    existing = repository.get_user_reaction(
        message_id,
        user_id,
        data.emoji,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already added this reaction",
        )

    reaction = repository.create(
        message_id=message_id,
        user_id=user_id,
        emoji=data.emoji,
    )

    response = MessageReactionResponse.model_validate(
        reaction
    )

    await connection_manager.broadcast(
        message.channel_id,
        {
            "type": "reaction_added",
            "id": reaction.id,
            "message_id": reaction.message_id,
            "user_id": reaction.user_id,
            "emoji": reaction.emoji,
            "created_at": reaction.created_at.isoformat(),
        },
    )

    return response


@router.get(
    "/{message_id}/reactions",
    response_model=list[MessageReactionResponse],
)
def list_reactions(
    message_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[MessageReactionResponse]:

    check_message_access(
        message_id,
        user_id,
        db,
    )

    repository = MessageReactionRepository(db)

    reactions = repository.get_message_reactions(
        message_id
    )

    return [
        MessageReactionResponse.model_validate(
            reaction
        )
        for reaction in reactions
    ]


@router.delete(
    "/{message_id}/reactions/{emoji}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_reaction(
    message_id: str,
    emoji: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:

    message = check_message_access(
        message_id,
        user_id,
        db,
    )

    repository = MessageReactionRepository(db)

    reaction = repository.get_user_reaction(
        message_id,
        user_id,
        emoji,
    )

    if reaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reaction not found",
        )

    repository.delete(reaction)

    await connection_manager.broadcast(
        message.channel_id,
        {
            "type": "reaction_removed",
            "message_id": message_id,
            "user_id": user_id,
            "emoji": emoji,
        },
    )

    return None