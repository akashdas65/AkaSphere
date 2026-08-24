from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.workspace_invitation_repository import (
    WorkspaceInvitationRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.workspace_invitation import (
    WorkspaceInvitationAccept,
    WorkspaceInvitationCreate,
    WorkspaceInvitationResponse,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Invitations"],
)


@router.post(
    "/{workspace_id}/invitations",
    response_model=WorkspaceInvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invitation(
    workspace_id: str,
    data: WorkspaceInvitationCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceInvitationResponse:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)
    invitation_repository = WorkspaceInvitationRepository(db)
    user_repository = UserRepository(db)

    workspace = workspace_repository.get_by_id(
        workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    current_membership = member_repository.get_membership(
        workspace_id,
        user_id,
    )

    if current_membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    if current_membership.role not in (
        "owner",
        "admin",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners and admins can invite members",
        )

    normalized_email = data.email.lower()

    existing_user = user_repository.get_by_email(
        normalized_email
    )

    if existing_user is not None:
        existing_membership = (
            member_repository.get_membership(
                workspace_id,
                existing_user.id,
            )
        )

        if existing_membership is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this workspace",
            )

    if (
        data.role == "admin"
        and current_membership.role != "owner"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can invite admins",
        )

    existing_invitation = (
        invitation_repository.get_active_by_email(
            workspace_id,
            normalized_email,
        )
    )

    if existing_invitation is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An active invitation already exists for this email",
        )

    token = token_urlsafe(32)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=7
    )

    invitation = invitation_repository.create(
        workspace_id=workspace_id,
        email=normalized_email,
        token=token,
        role=data.role,
        expires_at=expires_at,
    )

    return WorkspaceInvitationResponse.model_validate(
        invitation
    )


@router.post(
    "/invitations/accept",
    response_model=dict,
)
def accept_invitation(
    data: WorkspaceInvitationAccept,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:

    invitation_repository = WorkspaceInvitationRepository(
        db
    )
    member_repository = WorkspaceMemberRepository(db)
    user_repository = UserRepository(db)

    invitation = invitation_repository.get_by_token(
        data.token
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.accepted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has already been accepted",
        )

    if invitation.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has expired",
        )

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.email.lower() != invitation.email.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation was sent to a different email address",
        )

    existing_membership = member_repository.get_membership(
        invitation.workspace_id,
        user_id,
    )

    if existing_membership is not None:
        invitation_repository.mark_accepted(
            invitation
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this workspace",
        )

    member_repository.create(
        workspace_id=invitation.workspace_id,
        user_id=user_id,
        role=invitation.role,
    )

    invitation_repository.mark_accepted(
        invitation
    )

    return {
        "message": "Invitation accepted successfully",
        "workspace_id": invitation.workspace_id,
        "role": invitation.role,
    }