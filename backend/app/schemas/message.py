from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )


class MessageUpdate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel_id: str
    user_id: str
    content: str
    is_edited: bool
    created_at: datetime
    updated_at: datetime