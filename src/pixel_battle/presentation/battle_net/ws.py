from collections import defaultdict
from typing import AsyncIterable

from fastapi import WebSocket, WebSocketDisconnect


type ConnectionGroup = set[WebSocket]
type ConnectionGroupID = tuple[int, int]
type ConnectionGroupByGroupID = defaultdict[ConnectionGroupID, ConnectionGroup]


async def texts_and_then_disconnect_of(
    connection: WebSocket,
    *,
    its_group: ConnectionGroup | None = None,
) -> AsyncIterable[str]:
    try:
        async for text in connection.iter_text():
            yield text
    except WebSocketDisconnect:
        if its_group is not None:
            its_group.remove(connection)
