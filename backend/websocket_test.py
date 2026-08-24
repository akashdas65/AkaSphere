import asyncio
import json

import websockets


USER_ID = "bbe7d49b-e72d-4bef-8ef7-2df1850e54b2"
CHANNEL_ID = "cfe15bc9-a335-47a4-bedd-fc2cf645c0b5"

URL = (
    f"ws://127.0.0.1:8000/api/v1/ws/channels/"
    f"{CHANNEL_ID}?user_id={USER_ID}"
)


async def main():
    async with websockets.connect(URL) as websocket:

        print("Connected to AkaSphere WebSocket")

        # Receive "User joined the channel" event
        response = await websocket.recv()

        print("Received:")
        print(json.dumps(
            json.loads(response),
            indent=2,
        ))

        # Send a message
        await websocket.send(
            json.dumps({
                "content": "Hello from WebSocket!"
            })
        )

        # Receive broadcast message
        response = await websocket.recv()

        print("Message received:")
        print(json.dumps(
            json.loads(response),
            indent=2,
        ))


if __name__ == "__main__":
    asyncio.run(main())