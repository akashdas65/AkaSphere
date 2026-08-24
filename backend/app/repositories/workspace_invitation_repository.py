from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace_invitation import WorkspaceInvitation


class WorkspaceInvitationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_token(
        self,
        token: str,
    ) -> WorkspaceInvitation | None:
        statement = select(WorkspaceInvitation).where(
            WorkspaceInvitation.token == token
        )

        return self.db.scalar(statement)

    def get_active_by_email(
        self,
        workspace_id: str,
        email: str,
    ) -> WorkspaceInvitation | None:
        statement = (
            select(WorkspaceInvitation)
            .where(
                WorkspaceInvitation.workspace_id == workspace_id,
                WorkspaceInvitation.email == email,
                WorkspaceInvitation.accepted_at.is_(None),
                WorkspaceInvitation.expires_at > datetime.now(timezone.utc),
            )
            .order_by(
                WorkspaceInvitation.created_at.desc()
            )
        )

        return self.db.scalar(statement)

    def create(
        self,
        workspace_id: str,
        email: str,
        token: str,
        role: str,
        expires_at: datetime,
    ) -> WorkspaceInvitation:
        invitation = WorkspaceInvitation(
            workspace_id=workspace_id,
            email=email,
            token=token,
            role=role,
            expires_at=expires_at,
        )

        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)

        return invitation

    def mark_accepted(
        self,
        invitation: WorkspaceInvitation,
    ) -> WorkspaceInvitation:
        invitation.accepted_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(invitation)

        return invitation