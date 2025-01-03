from asyncio import gather
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Iterable

from fastapi import WebSocket, status

from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema


type WebsocketGroup = set[WebSocket]
type WebsocketGroupID = tuple[int, int]


@dataclass(init=False)
class Streaming:
    __view_chunk_stream: ViewChunkStream
    __websocket_group_by_group_id: dict[WebsocketGroupID, WebsocketGroup]

    def __init__(self, view_chunk_stream: ViewChunkStream) -> None:
        self.__view_chunk_stream = view_chunk_stream
        self.__websocket_group_by_group_id = defaultdict(set)

    @asynccontextmanager
    async def __enter__(self) -> AsyncIterator["Streaming"]:
        try:
            yield self
        except Exception:
            await self.stop(panic=True)
        else:
            await self.stop(panic=False)

    def add_client(
        self, *, websocket: WebSocket, group_id: WebsocketGroupID
    ) -> None:
        self.__websocket_group_by_group_id[group_id].add(websocket)

    @property
    def __group_id_cycle(self) -> Iterable[WebsocketGroupID]:
        while True:
            yield from tuple(self.__websocket_group_by_group_id.keys())

    async def start(self) -> None:
        for x, y in self.__group_id_cycle:
            result = await self.__view_chunk_stream(x, y)

            if len(result.new_pixels) == 0:
                continue

            response_model = RecoloredPixelListSchema.of(result.new_pixels)
            response = response_model.model_dump_json()

            websockets = self.__websocket_group_by_group_id[x, y]

            await gather(*(
                websocket.send_text(response)
                for websocket in websockets
            ))

    async def stop(self, *, panic: bool) -> None:
        await gather(*(
            self.__remove_client(
                websocket=websocket, group_id=group_id, panic=panic
            )
            for group_id, group in self.__websocket_group_by_group_id.items()
            for websocket in group
        ))

    async def __remove_client(
        self, *, websocket: WebSocket, group_id: WebsocketGroupID, panic: bool
    ) -> None:
        self.__websocket_group_by_group_id[group_id].remove(websocket)

        code = (
            status.WS_1011_INTERNAL_ERROR
            if panic
            else status.WS_1000_NORMAL_CLOSURE
        )

        await websocket.close(code)
