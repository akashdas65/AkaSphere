from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageReactionCreate(BaseModel):
    emoji: str = Field(
        min_length=1,
        max_length=50,
    )


class MessageReactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    message_id: str
    user_id: str
    emoji: str
    created_at: datetime