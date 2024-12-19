from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from operator import add
from typing import (
    AsyncIterator,
    Iterable,
    Iterator,
    Sequence,
)

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.broker import Broker, NewPixelStateEvent
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, RGBColorValue
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.redis_cluster.keys import chunk_key_of


@dataclass(init=False)
class InMemoryBroker(Broker):
    __pixels_by_chunk: defaultdict[Chunk, list[Pixel[RGBColor]]]
    __offset_by_chunk: defaultdict[Chunk, int]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        self.__pixels_by_chunk = defaultdict(list)
        self.__offset_by_chunk = defaultdict(lambda: 0)

        for pixel in pixels:
            self.__pixels_by_chunk[pixel.chunk].append(pixel)

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(chain.from_iterable(self.__pixels_by_chunk.values()))

    def __len__(self) -> int:
        return reduce(add, map(len, self.__pixels_by_chunk.values()))

    def __bool__(self) -> bool:
        return any(map(bool, self.__pixels_by_chunk.values()))

    async def add_event_with(self, *, pixel: Pixel[RGBColor]) -> None:
        self.__pixels_by_chunk[pixel.chunk].append(pixel)

    async def events_from(
        self, offset: int, *, chunk: Chunk
    ) -> Sequence[NewPixelStateEvent]:
        pixels = self.__pixels_by_chunk[chunk][offset + 1:]
        return tuple(
            NewPixelStateEvent(pixel=pixel, offset=index + offset + 1)
            for index, pixel in enumerate(pixels)
        )

    @asynccontextmanager
    async def new_events_of(
        self, chunk: Chunk
    ) -> AsyncIterator[Sequence[NewPixelStateEvent]]:
        offset = self.__offset_by_chunk[chunk]

        yield await self.events_from(offset, chunk=chunk)

        self.__offset_by_chunk[chunk] = len(self.__pixels_by_chunk[chunk])


type RedisStreamEvent = tuple[bytes, dict[bytes, bytes]]
type RedisStreamEvents = list[RedisStreamEvent]
type RedisStreamKeyAndEvents = tuple[bytes, RedisStreamEvents]


@dataclass(kw_only=True, frozen=True, slots=True)
class _RedisClusterStreamBroker(Broker):
    redis_cluster: RedisCluster

    async def add_event_with(self, *, pixel: Pixel[RGBColor]) -> None:
        key = self._key_by(pixel.chunk)
        mapping = self.__mapping_of(pixel)

        await self.redis_cluster.xadd(key, mapping, limit=5_000_000)  # type: ignore[misc]

    async def events_from(
        self, offset: int, *, chunk: Chunk
    ) -> Sequence[NewPixelStateEvent]:
        key = self._key_by(chunk)

        raw_events: RedisStreamEvents
        raw_events = await self.redis_cluster.xrange(key, offset + 1)

        return tuple(map(self._event_of, raw_events))

    @asynccontextmanager
    async def new_events_of(
        self, chunk: Chunk
    ) -> AsyncIterator[Sequence[NewPixelStateEvent]]:
        key = self.__key_by(chunk)
        result = await self.redis_cluster.xread({key: "$"}, block=10000)
        raw_events: RedisStreamEvents = result[0][0]

        yield tuple(map(self.__event_of, raw_events))

    def _key_by(self, chunk: Chunk) -> bytes:
        return chunk_key_of(chunk) + bytes(["stream"])

    def _event_of(self, raw_event: RedisStreamEvent) -> NewPixelStateEvent:
        return NewPixelStateEvent(
            pixel=self.__raw_event_pixel_of(raw_event),
            offset=self.__raw_event_offset_of(raw_event),
        )

    def __mapping_of(self, pixel: Pixel[RGBColor]) -> dict[bytes, bytes]:
        return {bytes(0): self.__encoded(pixel)}

    def __mapping_pixel_of(
        self, mapping: dict[bytes, bytes]
    ) -> Pixel[RGBColor]:
        return self.__decoded(mapping[bytes(0)])

    def __encoded(self, pixel: Pixel[RGBColor]) -> bytes:
        return bytes([
            pixel.position_within_chunk.x * 10 + pixel.position_within_chunk.y,
            pixel.color.red.number,
            pixel.color.green.number,
            pixel.color.blue.number,
        ])

    def __decoded(self, bytes_: bytes, *, chunk: Chunk) -> Pixel[RGBColor]:
        position_within_chunk_x = bytes_[0] // 10
        position_within_chunk_y = bytes_[0] - position_within_chunk_x
        position_within_chunk = Vector(
            x=position_within_chunk_x, y=position_within_chunk_y
        )
        position = position_within_chunk + chunk.area.min_x_min_y_position

        red = RGBColorValue(number=bytes_[1])
        green = RGBColorValue(number=bytes_[2])
        blue = RGBColorValue(number=bytes_[3])
        color = RGBColor(red=red, green=green, blue=blue)

        return Pixel(position=position, color=color)

    def __raw_event_offset_of(self, raw_event: RedisStreamEvent) -> int:
        return int(raw_event[0].decode().split("-")[0])

    def __raw_event_pixel_of(self, raw_event: RedisStreamEvent) -> Pixel:
        return self.__mapping_pixel_of(raw_event[1])
