from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

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


@router.websocket(
    "/channels/{channel_id}"
)
async def channel_websocket(
    websocket: WebSocket,
    channel_id: str,
):
    db: Session = SessionLocal()

    try:
        user_id = websocket.query_params.get(
            "user_id"
        )

        if not user_id:
            await websocket.close(
                code=1008,
                reason="Authentication required",
            )
            return

        member_repository = WorkspaceMemberRepository(
            db
        )

        message_repository = MessageRepository(
            db
        )

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

        await connection_manager.connect(
            channel_id,
            websocket,
        )

        await connection_manager.broadcast(
            channel_id,
            {
                "type": "system",
                "message": "User joined the channel",
                "user_id": user_id,
            },
        )

        while True:
            data = await websocket.receive_json()

            content = data.get(
                "content",
                "",
            )

            content = content.strip()

            if not content:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Message content cannot be empty",
                    }
                )
                continue

            saved_message = message_repository.create(
                channel_id=channel_id,
                user_id=user_id,
                content=content,
            )

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

            await connection_manager.broadcast(
                channel_id,
                message,
            )

    except WebSocketDisconnect:
        connection_manager.disconnect(
            channel_id,
            websocket,
        )

    except Exception:
        connection_manager.disconnect(
            channel_id,
            websocket,
        )

    finally:
        db.close()