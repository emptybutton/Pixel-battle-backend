from asyncio import Event, gather
from collections import defaultdict
from collections.abc import AsyncIterable, AsyncIterator
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass

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
    disconnection_event: Event


@dataclass(init=False)
class Streaming:
    __view_chunk_stream: ViewChunkStream
    __client_group_by_group_id: dict[
        StreamingClientGroupID, set[StreamingClient]
    ]

    def __init__(self, view_chunk_stream: ViewChunkStream) -> None:
        self.__view_chunk_stream = view_chunk_stream
        self.__client_group_by_group_id = defaultdict(set)
        self.__group_id_iteration_event = Event()

    def add_client(self, client: StreamingClient) -> None:
        self.__client_group_by_group_id[client.group_id].add(client)
        self.__group_id_iteration_event.set()

    async def start(self) -> None:
        async with self.__finalization():
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

    @asynccontextmanager
    async def __finalization(self) -> AsyncIterator[None]:
        try:
            yield
        except Exception as error:
            await self.__finalize(panic=True)
            raise error from error
        else:
            await self.__finalize(panic=False)

    async def __finalize(self, *, panic: bool) -> None:
        await gather(*(
            self.__disconnect_client(client, panic=panic)
            for _, group in self.__client_group_by_group_id.items()
            for client in group
        ))

    async def __send(self, response: str, *, client: StreamingClient) -> None:
        try:
            await client.websocket.send_text(response)
        except WebSocketDisconnect:
            self.__handle_client_disconnect(client)

    async def __group_id_cycle(self) -> AsyncIterable[StreamingClientGroupID]:
        while True:
            await self.__group_id_iteration_event.wait()

            for client_id in self.__client_group_by_group_id:
                yield client_id

    async def __disconnect_client(
        self, client: StreamingClient, panic: bool
    ) -> None:
        code = (
            status.WS_1011_INTERNAL_ERROR
            if panic
            else status.WS_1000_NORMAL_CLOSURE
        )
        with suppress(WebSocketDisconnect):
            await client.websocket.close(code)

        self.__handle_client_disconnect(client)

    def __handle_client_disconnect(self, client: StreamingClient) -> None:
        self.__remove_client(client)
        client.disconnection_event.set()

    def __has_clients(self) -> bool:
        return bool(tuple(self.__client_group_by_group_id.values()))

    def __remove_client(self, client: StreamingClient) -> None:
        self.__client_group_by_group_id[client.group_id].remove(client)

        if not self.__has_clients():
            self.__group_id_iteration_event.clear()
