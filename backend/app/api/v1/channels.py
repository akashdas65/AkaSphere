from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.channel_repository import ChannelRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.channel import (
    ChannelCreate,
    ChannelResponse,
    ChannelUpdate,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Channels"],
)


@router.post(
    "/{workspace_id}/channels",
    response_model=ChannelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_channel(
    workspace_id: str,
    data: ChannelCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ChannelResponse:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)
    channel_repository = ChannelRepository(db)

    workspace = workspace_repository.get_by_id(
        workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    if membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners and admins can create channels",
        )

    existing = channel_repository.get_by_slug(
        workspace_id,
        data.slug,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Channel slug already exists in this workspace",
        )

    channel = channel_repository.create(
        workspace_id=workspace_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        is_private=data.is_private,
    )

    return ChannelResponse.model_validate(channel)


@router.get(
    "/{workspace_id}/channels",
    response_model=list[ChannelResponse],
)
def list_channels(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[ChannelResponse]:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)
    channel_repository = ChannelRepository(db)

    workspace = workspace_repository.get_by_id(
        workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    channels = channel_repository.get_workspace_channels(
        workspace_id
    )

    return [
        ChannelResponse.model_validate(channel)
        for channel in channels
    ]


@router.get(
    "/{workspace_id}/channels/{channel_id}",
    response_model=ChannelResponse,
)
def get_channel(
    workspace_id: str,
    channel_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ChannelResponse:

    member_repository = WorkspaceMemberRepository(db)
    channel_repository = ChannelRepository(db)

    membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    channel = channel_repository.get_by_id(
        channel_id
    )

    if (
        channel is None
        or not channel.is_active
        or channel.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    return ChannelResponse.model_validate(channel)


@router.patch(
    "/{workspace_id}/channels/{channel_id}",
    response_model=ChannelResponse,
)
def update_channel(
    workspace_id: str,
    channel_id: str,
    data: ChannelUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ChannelResponse:

    member_repository = WorkspaceMemberRepository(db)
    channel_repository = ChannelRepository(db)

    membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    if membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners and admins can update channels",
        )

    channel = channel_repository.get_by_id(
        channel_id
    )

    if (
        channel is None
        or not channel.is_active
        or channel.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    updated_channel = channel_repository.update(
        channel=channel,
        name=data.name,
        description=data.description,
        is_private=data.is_private,
    )

    return ChannelResponse.model_validate(
        updated_channel
    )


@router.delete(
    "/{workspace_id}/channels/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_channel(
    workspace_id: str,
    channel_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:

    member_repository = WorkspaceMemberRepository(db)
    channel_repository = ChannelRepository(db)

    membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    if membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners and admins can archive channels",
        )

    channel = channel_repository.get_by_id(
        channel_id
    )

    if (
        channel is None
        or not channel.is_active
        or channel.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    channel_repository.delete(channel)

    return None