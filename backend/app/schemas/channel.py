from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChannelCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    slug: str = Field(
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    is_private: bool = False


class ChannelUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    is_private: bool = False


class ChannelResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: str
    workspace_id: str
    name: str
    slug: str
    description: str | None
    is_private: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime