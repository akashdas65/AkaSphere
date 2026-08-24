from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[
            str,
            list[WebSocket],
        ] = defaultdict(list)

    async def connect(
        self,
        channel_id: str,
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()

        self.active_connections[
            channel_id
        ].append(websocket)

    def disconnect(
        self,
        channel_id: str,
        websocket: WebSocket,
    ) -> None:
        connections = self.active_connections.get(
            channel_id,
            [],
        )

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(
                channel_id,
                None,
            )

    async def broadcast(
        self,
        channel_id: str,
        message: dict,
    ) -> None:
        connections = self.active_connections.get(
            channel_id,
            [],
        )

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(
                channel_id,
                websocket,
            )


connection_manager = ConnectionManager()