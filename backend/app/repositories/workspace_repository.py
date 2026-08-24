from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        workspace_id: str,
    ) -> Workspace | None:

        statement = select(Workspace).where(
            Workspace.id == workspace_id
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Workspace | None:

        statement = select(Workspace).where(
            Workspace.slug == slug
        )

        return self.db.scalar(statement)

    def get_user_workspaces(
        self,
        user_id: str,
    ) -> list[Workspace]:

        statement = (
            select(Workspace)
            .join(
                WorkspaceMember,
                WorkspaceMember.workspace_id == Workspace.id,
            )
            .where(
                WorkspaceMember.user_id == user_id,
                Workspace.is_active.is_(True),
            )
            .order_by(Workspace.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        name: str,
        slug: str,
        description: str | None,
        owner_id: str,
    ) -> Workspace:

        workspace = Workspace(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
        )

        self.db.add(workspace)
        self.db.flush()

        owner_membership = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=owner_id,
            role="owner",
        )

        self.db.add(owner_membership)

        self.db.commit()
        self.db.refresh(workspace)

        return workspace

    def delete(
        self,
        workspace: Workspace,
    ) -> None:

        workspace.is_active = False

        self.db.commit()