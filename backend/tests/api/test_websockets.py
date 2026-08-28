from fastapi.routing import APIWebSocketRoute

from app.main import app


def test_websocket_module_is_registered():
    websocket_routes = []

    for route in app.routes:
        if isinstance(route, APIWebSocketRoute):
            websocket_routes.append(route.path)

        elif hasattr(route, "original_router"):
            for nested_route in route.original_router.routes:
                if isinstance(nested_route, APIWebSocketRoute):
                    prefix = route.include_context.prefix
                    websocket_routes.append(
                        f"{prefix}{nested_route.path}"
                    )

    assert "/api/v1/ws/channels/{channel_id}" in websocket_routes