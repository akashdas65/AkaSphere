from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.db.session import get_db
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace(
    data: WorkspaceCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:

    repository = WorkspaceRepository(db)

    existing = repository.get_by_slug(
        data.slug
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workspace slug already exists",
        )

    workspace = repository.create(
        name=data.name,
        slug=data.slug,
        description=data.description,
        owner_id=user_id,
    )

    return WorkspaceResponse.model_validate(
        workspace
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
def list_workspaces(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[WorkspaceResponse]:

    repository = WorkspaceRepository(db)

    workspaces = repository.get_user_workspaces(
        user_id
    )

    return [
        WorkspaceResponse.model_validate(workspace)
        for workspace in workspaces
    ]


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:

    repository = WorkspaceRepository(db)

    workspace = repository.get_by_id(
        workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    # Owner can always access the workspace.
    if workspace.owner_id == user_id:
        return WorkspaceResponse.model_validate(
            workspace
        )

    user_workspaces = repository.get_user_workspaces(
        user_id
    )

    if not any(
        item.id == workspace.id
        for item in user_workspaces
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    return WorkspaceResponse.model_validate(
        workspace
    )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:

    repository = WorkspaceRepository(db)

    workspace = repository.get_by_id(
        workspace_id
    )

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    if workspace.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can delete it",
        )

    repository.delete(workspace)

    return None