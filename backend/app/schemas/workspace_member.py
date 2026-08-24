from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workspace_id: str
    user_id: str
    role: str
    joined_at: datetime


class WorkspaceMemberRoleUpdate(BaseModel):
    role: str = Field(
        pattern=r"^(admin|member)$"
    )