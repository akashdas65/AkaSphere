from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace_member import WorkspaceMember


class WorkspaceMemberRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        member_id: str,
    ) -> WorkspaceMember | None:

        statement = select(WorkspaceMember).where(
            WorkspaceMember.id == member_id
        )

        return self.db.scalar(statement)

    def get_members(
        self,
        workspace_id: str,
    ) -> list[WorkspaceMember]:

        statement = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id
                == workspace_id
            )
            .order_by(
                WorkspaceMember.joined_at.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_membership(
        self,
        workspace_id: str,
        user_id: str,
    ) -> WorkspaceMember | None:

        statement = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id
            == workspace_id,
            WorkspaceMember.user_id == user_id,
        )

        return self.db.scalar(statement)

    def add_member(
        self,
        workspace_id: str,
        user_id: str,
        role: str = "member",
    ) -> WorkspaceMember:

        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)

        return member

    def update_role(
        self,
        member: WorkspaceMember,
        role: str,
    ) -> WorkspaceMember:

        member.role = role

        self.db.commit()
        self.db.refresh(member)

        return member

    def remove_member(
        self,
        member: WorkspaceMember,
    ) -> None:

        self.db.delete(member)
        self.db.commit()