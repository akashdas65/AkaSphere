from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class WorkspaceInvitationCreate(BaseModel):
    email: EmailStr

    role: str = Field(
        default="member",
        pattern=r"^(member|admin)$",
    )


class WorkspaceInvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workspace_id: str
    email: EmailStr
    token: str
    role: str
    expires_at: datetime
    created_at: datetime
    accepted_at: datetime | None


class WorkspaceInvitationAccept(BaseModel):
    token: str = Field(
        min_length=20,
        max_length=255,
    )