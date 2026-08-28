from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.channels import router as channels_router
from app.api.v1.messages import router as messages_router
from app.api.v1.message_reactions import (
    router as message_reactions_router,
)
from app.api.v1.websockets import router as websocket_router
from app.api.v1.workspaces import router as workspaces_router
from app.api.v1.workspace_invitations import (
    router as workspace_invitations_router,
)
from app.api.v1.workspace_members import (
    router as workspace_members_router,
)


app = FastAPI(
    title="AkaSphere API",
    description="AI-powered collaboration platform",
    version="0.1.0",
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    workspaces_router,
    prefix="/api/v1",
)

app.include_router(
    workspace_members_router,
    prefix="/api/v1",
)

app.include_router(
    workspace_invitations_router,
    prefix="/api/v1",
)

app.include_router(
    channels_router,
    prefix="/api/v1",
)

app.include_router(
    messages_router,
    prefix="/api/v1",
)

app.include_router(
    message_reactions_router,
    prefix="/api/v1",
)

app.include_router(
    websocket_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "akasphere-api",
        "version": "0.1.0",
    }