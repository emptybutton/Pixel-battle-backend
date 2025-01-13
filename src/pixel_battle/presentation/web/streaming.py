from asyncio import Event, gather
from collections import defaultdict
from dataclasses import dataclass
from types import TracebackType
from typing import AsyncIterable, Self, Type

from fastapi import WebSocket, WebSocketDisconnect, status

from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema


type StreamingClientGroupID = tuple[int, int]


@dataclass(kw_only=True, frozen=True, slots=True)
class StreamingClient:
    websocket: WebSocket
    group_id: StreamingClientGroupID


@dataclass(init=False)
class Streaming:
    __view_chunk_stream: ViewChunkStream
    __client_group_by_group_id: dict[
        StreamingClientGroupID, set[StreamingClient]
    ]

    def __init__(self, view_chunk_stream: ViewChunkStream) -> None:
        self.__view_chunk_stream = view_chunk_stream
        self.__client_group_by_group_id = defaultdict(set)
        self.__client_existence_event = Event()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.stop(panic=error is not None)

    def add_client(self, client: StreamingClient) -> None:
        self.__client_group_by_group_id[client.group_id].add(client)
        self.__client_existence_event.set()

    async def start(self) -> None:
        async for x, y in self.__group_id_cycle():
            result = await self.__view_chunk_stream(x, y)

            if len(result.new_pixels) == 0:
                continue

            response_model = RecoloredPixelListSchema.of(result.new_pixels)
            response = response_model.model_dump_json()

            client_group = self.__client_group_by_group_id[x, y]

            await gather(*(
                self.__send(response, client=client)
                for client in client_group
            ))

    async def stop(self, *, panic: bool) -> None:
        await gather(*(
            self.__disconnect_client(client, panic=panic)
            for group_id, group in self.__client_group_by_group_id.items()
            for client in group
        ))

    async def __send(self, response: str, *, client: StreamingClient) -> None:
        try:
            await client.websocket.send_text(response)
        except WebSocketDisconnect:
            self.__remove_client(client)

    async def __group_id_cycle(self) -> AsyncIterable[StreamingClientGroupID]:
        while True:
            await self.__client_existence_event.wait()

            for client_id in self.__client_group_by_group_id:
                yield client_id

    async def __disconnect_client(
        self, client: StreamingClient, panic: bool
    ) -> None:
        self.__remove_client(client)

        code = (
            status.WS_1011_INTERNAL_ERROR
            if panic
            else status.WS_1000_NORMAL_CLOSURE
        )
        await client.websocket.close(code)

    def __has_clients(self) -> bool:
        return bool(tuple(self.__client_group_by_group_id.values()))

    def __remove_client(self, client: StreamingClient) -> None:
        self.__client_group_by_group_id[client.group_id].remove(client)

        if not self.__has_clients():
            self.__client_existence_event.clear()
