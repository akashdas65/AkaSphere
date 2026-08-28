from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.repositories.message_repository import MessageRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.services.websocket_manager import connection_manager


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


def authenticate_websocket(
    websocket: WebSocket,
) -> str | None:
    """
    Authenticate a WebSocket connection using a JWT access token.

    Supported format:

        /ws/channels/{channel_id}?token=<access_token>

    Returns the authenticated user ID or None when authentication fails.
    """

    token = websocket.query_params.get("token")

    if not token:
        return None

    try:
        payload = decode_token(token)
    except ValueError:
        return None

    if payload.get("type") != "access":
        return None

    user_id = payload.get("sub")

    if not user_id:
        return None

    return str(user_id)


@router.websocket(
    "/channels/{channel_id}"
)
async def channel_websocket(
    websocket: WebSocket,
    channel_id: str,
):
    db: Session = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Authenticate user using JWT
        # ---------------------------------------------------------

        user_id = authenticate_websocket(websocket)

        if not user_id:
            await websocket.close(
                code=1008,
                reason="Authentication required",
            )
            return

        # ---------------------------------------------------------
        # 2. Load repositories
        # ---------------------------------------------------------

        member_repository = WorkspaceMemberRepository(db)
        message_repository = MessageRepository(db)

        # ---------------------------------------------------------
        # 3. Check channel
        # ---------------------------------------------------------

        from app.models.channel import Channel

        channel = db.get(
            Channel,
            channel_id,
        )

        if channel is None or not channel.is_active:
            await websocket.close(
                code=1008,
                reason="Channel not found",
            )
            return

        # ---------------------------------------------------------
        # 4. Check workspace membership
        # ---------------------------------------------------------

        membership = member_repository.get_membership(
            channel.workspace_id,
            user_id,
        )

        if membership is None:
            await websocket.close(
                code=1008,
                reason="You are not a member of this workspace",
            )
            return

        # ---------------------------------------------------------
        # 5. Private channel access
        # ---------------------------------------------------------

        if channel.is_private and membership.role not in (
            "owner",
            "admin",
        ):
            await websocket.close(
                code=1008,
                reason="You do not have access to this private channel",
            )
            return

        # ---------------------------------------------------------
        # 6. Register WebSocket connection
        # ---------------------------------------------------------

        await connection_manager.connect(
            channel_id,
            websocket,
        )

        # ---------------------------------------------------------
        # 7. Notify channel that user joined
        # ---------------------------------------------------------

        await connection_manager.broadcast(
            channel_id,
            {
                "type": "system",
                "event": "user_joined",
                "message": "User joined the channel",
                "user_id": user_id,
                "channel_id": channel_id,
            },
        )

        # ---------------------------------------------------------
        # 8. Receive messages
        # ---------------------------------------------------------

        while True:
            data = await websocket.receive_json()

            # -----------------------------------------------------
            # Validate incoming payload
            # -----------------------------------------------------

            if not isinstance(data, dict):
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid message payload",
                    }
                )
                continue

            content = data.get(
                "content",
                "",
            )

            if not isinstance(content, str):
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Message content must be a string",
                    }
                )
                continue

            content = content.strip()

            if not content:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Message content cannot be empty",
                    }
                )
                continue

            if len(content) > 5000:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Message content cannot exceed 5000 characters",
                    }
                )
                continue

            # -----------------------------------------------------
            # Save message to PostgreSQL
            # -----------------------------------------------------

            saved_message = message_repository.create(
                channel_id=channel_id,
                user_id=user_id,
                content=content,
            )

            # -----------------------------------------------------
            # Build broadcast payload
            # -----------------------------------------------------

            message = {
                "type": "message",
                "id": saved_message.id,
                "user_id": saved_message.user_id,
                "channel_id": saved_message.channel_id,
                "content": saved_message.content,
                "is_edited": saved_message.is_edited,
                "created_at": (
                    saved_message.created_at.isoformat()
                    if saved_message.created_at
                    else None
                ),
                "updated_at": (
                    saved_message.updated_at.isoformat()
                    if saved_message.updated_at
                    else None
                ),
            }

            # -----------------------------------------------------
            # Broadcast message to everyone in channel
            # -----------------------------------------------------

            await connection_manager.broadcast(
                channel_id,
                message,
            )

    except WebSocketDisconnect:
        connection_manager.disconnect(
            channel_id,
            websocket,
        )

        await connection_manager.broadcast(
            channel_id,
            {
                "type": "system",
                "event": "user_left",
                "message": "User left the channel",
                "user_id": user_id if "user_id" in locals() else None,
                "channel_id": channel_id,
            },
        )

    except Exception:
        connection_manager.disconnect(
            channel_id,
            websocket,
        )

    finally:
        db.close()