from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.message_repository import MessageRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageUpdate,
)


router = APIRouter(
    prefix="/channels",
    tags=["Messages"],
)


def check_channel_access(
    channel_id: str,
    user_id: str,
    db: Session,
):
    from app.models.channel import Channel

    channel = db.get(Channel, channel_id)

    if channel is None or not channel.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)

    workspace = workspace_repository.get_by_id(
        channel.workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
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

    if channel.is_private and membership.role not in (
        "owner",
        "admin",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this private channel",
        )

    return channel


@router.post(
    "/{channel_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    channel_id: str,
    data: MessageCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MessageResponse:

    check_channel_access(
        channel_id,
        user_id,
        db,
    )

    repository = MessageRepository(db)

    message = repository.create(
        channel_id=channel_id,
        user_id=user_id,
        content=data.content,
    )

    return MessageResponse.model_validate(
        message
    )


@router.get(
    "/{channel_id}/messages",
    response_model=list[MessageResponse],
)
def list_messages(
    channel_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[MessageResponse]:

    check_channel_access(
        channel_id,
        user_id,
        db,
    )

    repository = MessageRepository(db)

    messages = repository.get_channel_messages(
        channel_id
    )

    return [
        MessageResponse.model_validate(message)
        for message in messages
    ]


@router.get(
    "/{channel_id}/messages/{message_id}",
    response_model=MessageResponse,
)
def get_message(
    channel_id: str,
    message_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MessageResponse:

    check_channel_access(
        channel_id,
        user_id,
        db,
    )

    repository = MessageRepository(db)

    message = repository.get_by_id(
        message_id
    )

    if (
        message is None
        or message.channel_id != channel_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return MessageResponse.model_validate(
        message
    )


@router.patch(
    "/{channel_id}/messages/{message_id}",
    response_model=MessageResponse,
)
def update_message(
    channel_id: str,
    message_id: str,
    data: MessageUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MessageResponse:

    check_channel_access(
        channel_id,
        user_id,
        db,
    )

    repository = MessageRepository(db)

    message = repository.get_by_id(
        message_id
    )

    if (
        message is None
        or message.channel_id != channel_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    if message.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own messages",
        )

    updated_message = repository.update(
        message,
        data.content,
    )

    return MessageResponse.model_validate(
        updated_message
    )


@router.delete(
    "/{channel_id}/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_message(
    channel_id: str,
    message_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:

    check_channel_access(
        channel_id,
        user_id,
        db,
    )

    repository = MessageRepository(db)

    message = repository.get_by_id(
        message_id
    )

    if (
        message is None
        or message.channel_id != channel_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    if message.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own messages",
        )

    repository.delete(message)

    return None