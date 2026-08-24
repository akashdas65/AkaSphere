from fastapi import APIRouter

from app.api.v1.websockets import router as websocket_router
from app.api.v1.messages import router as messages_router
from app.api.v1.message_reactions import (
    router as message_reactions_router,
)
from app.api.v1.channels import router as channels_router
from app.api.v1.auth import router as auth_router
from app.api.v1.workspace_invitations import (
    router as workspace_invitations_router,
)
from app.api.v1.workspace_members import (
    router as workspace_members_router,
)
from app.api.v1.workspaces import (
    router as workspaces_router,
)


api_router = APIRouter()


api_router.include_router(
    auth_router,
)

api_router.include_router(
    workspaces_router,
)

api_router.include_router(
    workspace_members_router,
)

api_router.include_router(
    workspace_invitations_router,
)

api_router.include_router(
    channels_router,
)

api_router.include_router(
    messages_router,
)

api_router.include_router(
    message_reactions_router,
)

api_router.include_router(
    websocket_router,
)