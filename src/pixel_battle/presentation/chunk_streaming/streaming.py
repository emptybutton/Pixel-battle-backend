from asyncio import gather
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from itertools import cycle, product
from typing import AsyncIterator, Iterable

from fastapi import WebSocket, status
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


class RecoloredPixelSchema(BaseModel):
    pixel_position: tuple[int, int] | None = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] | None = Field(alias="newPixelColor")

    @classmethod
    def of(cls, pixel: Pixel[RGBColor]) -> "RecoloredPixelSchema":
        pixel_position = (pixel.position.x, pixel.position.y)
        new_pixel_color = (
            pixel.color.red.number,
            pixel.color.green.number,
            pixel.color.blue.number,
        )

        return RecoloredPixelSchema(
            pixelPosition=pixel_position, newPixelColor=new_pixel_color
        )


class RecoloredPixelListSchema(BaseModel):
    pixels: list[RecoloredPixelSchema]

    @classmethod
    def of(
        cls, pixels: Iterable[Pixel[RGBColor]]
    ) -> "RecoloredPixelListSchema":
        pixels = list(map(RecoloredPixelSchema.of, pixels))

        return RecoloredPixelListSchema(pixels=pixels)


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

    async def __call__(self) -> None:
        for x, y in cycle(product(range(10), repeat=2)):
            result = await self.__view_chunk_stream(x, y)

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
