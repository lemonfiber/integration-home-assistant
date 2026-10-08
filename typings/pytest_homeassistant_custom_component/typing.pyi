# Copyright (c) 2026 NightWorksIO
# The websocket client the harness hands a test, with the types it has.

from collections.abc import Callable, Coroutine
from typing import Any

from aiohttp import ClientWebSocketResponse

class MockHAClientWebSocket(ClientWebSocketResponse):
    send_json_auto_id: Callable[[dict[str, Any]], Coroutine[Any, Any, None]]

type WebSocketGenerator = Callable[..., Coroutine[Any, Any, MockHAClientWebSocket]]
