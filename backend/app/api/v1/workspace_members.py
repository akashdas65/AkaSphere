from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.workspace_member import (
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Members"],
)


@router.get(
    "/{workspace_id}/members",
    response_model=list[WorkspaceMemberResponse],
)
def list_members(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[WorkspaceMemberResponse]:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)

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

    members = member_repository.get_members(
        workspace_id
    )

    return [
        WorkspaceMemberResponse.model_validate(member)
        for member in members
    ]


@router.patch(
    "/{workspace_id}/members/{member_id}",
    response_model=WorkspaceMemberResponse,
)
def update_member_role(
    workspace_id: str,
    member_id: str,
    data: WorkspaceMemberRoleUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceMemberResponse:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)

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
            detail="Only owners and admins can change roles",
        )

    member = member_repository.get_by_id(
        member_id
    )

    if (
        member is None
        or member.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner role cannot be changed",
        )

    if data.role == "admin" and current_membership.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can promote members to admin",
        )

    updated_member = member_repository.update_role(
        member,
        data.role,
    )

    return WorkspaceMemberResponse.model_validate(
        updated_member
    )


@router.delete(
    "/{workspace_id}/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    workspace_id: str,
    member_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:

    workspace_repository = WorkspaceRepository(db)
    member_repository = WorkspaceMemberRepository(db)

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
            detail="Only owners and admins can remove members",
        )

    member = member_repository.get_by_id(
        member_id
    )

    if (
        member is None
        or member.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workspace owner cannot be removed",
        )

    if (
        member.role == "admin"
        and current_membership.role != "owner"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can remove an admin",
        )

    member_repository.remove_member(member)

    return None