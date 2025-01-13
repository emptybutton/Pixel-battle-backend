from asyncio import sleep
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import (
    AsyncIterator,
    Iterable,
    Iterator,
)

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.broker import Broker, NewPixelColorEvent
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.encoding import decoded, encoded
from pixel_battle.infrastructure.redis.keys import chunk_key_when
from pixel_battle.infrastructure.redis.types import (
    RedisStreamEvent,
    RedisStreamEventBody,
    RedisStreamEvents,
    RedisStreamOffset,
    RedisStreamResults,
)
from pixel_battle.infrastructure.types import Index


@dataclass(init=False)
class InMemoryBroker(Broker[Index]):
    __pixels_by_chunk: defaultdict[Chunk, list[Pixel[RGBColor]]]
    __first_unread_event_offset_by_chunk: dict[Chunk, Index]
    __first_pulling_timeout: int

    def __init__(
        self,
        pixels: Iterable[Pixel[RGBColor]] = tuple(),
        *,
        first_pulling_timeout: int = 1,
    ) -> None:
        self.__pixels_by_chunk = defaultdict(list)
        self.__first_pulling_timeout = first_pulling_timeout
        self.__first_unread_event_offset_by_chunk = dict()

        for pixel in pixels:
            self.__pixels_by_chunk[pixel.chunk].append(pixel)

    def __iter__(self) -> Iterator[tuple[Chunk, list[Pixel[RGBColor]]]]:
        return iter(tuple(
            (chunk, list(pixels))
            for chunk, pixels in self.__pixels_by_chunk.items()
        ))

    def __len__(self) -> int:
        return len(self.__pixels_by_chunk)

    def __bool__(self) -> bool:
        return bool(self.__pixels_by_chunk)

    async def push_event_with(self, *, pixel: Pixel[RGBColor]) -> None:
        self.__pixels_by_chunk[pixel.chunk].append(pixel)

    async def events_after(
        self, offset: Index, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[Index], ...]:
        return self.__events_from(offset + 1, chunk=chunk)

    @asynccontextmanager
    async def pulled_events_when(
        self, *, chunk: Chunk
    ) -> AsyncIterator[tuple[NewPixelColorEvent[Index], ...]]:
        unread_event_offset = self.__first_unread_event_offset_by_chunk.get(
            chunk
        )

        if unread_event_offset is None:
            unread_event_offset = len(self.__pixels_by_chunk[chunk])
            await sleep(self.__first_pulling_timeout)

        new_events = self.__events_from(unread_event_offset, chunk=chunk)

        yield new_events

        new_unread_event_offset = unread_event_offset + len(new_events)
        self.__first_unread_event_offset_by_chunk[chunk] = (
            new_unread_event_offset
        )

    async def events_when(
        self, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[Index], ...]:
        return tuple(
            NewPixelColorEvent(pixel=pixel, offset=offset)
            for offset, pixel in enumerate(self.__pixels_by_chunk[chunk])
        )

    def __events_from(
        self, offset: Index, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[Index], ...]:
        pixels = self.__pixels_by_chunk[chunk][offset:]

        return tuple(
            NewPixelColorEvent(pixel=pixel, offset=index + offset)
            for index, pixel in enumerate(pixels)
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisClusterStreamBroker(Broker[RedisStreamOffset]):
    redis_cluster: RedisCluster
    last_readed_event_offset_by_chunk: dict[Chunk, RedisStreamOffset] = (
        field(default_factory=dict)
    )

    async def push_event_with(self, *, pixel: Pixel[RGBColor]) -> None:
        key = self.__key_when(chunk=pixel.chunk)
        body = self.__event_body_of(pixel)

        await self.redis_cluster.xadd(key, body, maxlen=5_000_000)  # type: ignore[arg-type]

    async def events_after(
        self, offset: RedisStreamOffset, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[RedisStreamOffset], ...]:
        key = self.__key_when(chunk=chunk)

        results: RedisStreamResults
        results = await self.redis_cluster.xread({key: offset})

        return self.__result_list_events_of(results, chunk=chunk)

    async def events_when(
        self, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[RedisStreamOffset], ...]:
        key = self.__key_when(chunk=chunk)
        events: RedisStreamEvents = await self.redis_cluster.xrange(key)

        return self.__events_of(events, chunk=chunk)

    @asynccontextmanager
    async def pulled_events_when(
        self, *, chunk: Chunk
    ) -> AsyncIterator[tuple[NewPixelColorEvent[RedisStreamOffset], ...]]:
        offset = self.last_readed_event_offset_by_chunk.get(chunk) or b"$"
        key = self.__key_when(chunk=chunk)

        results: RedisStreamResults
        results = await self.redis_cluster.xread({key: offset}, block=3_000)

        events = self.__result_list_events_of(results, chunk=chunk)
        yield events

        if not events:
            return

        last_readed_event = events[-1]
        self.last_readed_event_offset_by_chunk[chunk] = last_readed_event.offset

    def __key_when(self, *, chunk: Chunk) -> bytes:
        return chunk_key_when(chunk=chunk) + b"stream"

    def __result_list_events_of(
        self, results: RedisStreamResults, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[RedisStreamOffset], ...]:
        if not results:
            return tuple()

        result = results[0]
        _, raw_events = result

        return self.__events_of(raw_events, chunk=chunk)

    def __events_of(
        self, raw_events: RedisStreamEvents, *, chunk: Chunk
    ) -> tuple[NewPixelColorEvent[RedisStreamOffset], ...]:
        return tuple(
            self.__event_of(raw_event, chunk=chunk) for raw_event in raw_events
        )

    def __event_of(
        self, raw_event: RedisStreamEvent, *, chunk: Chunk
    ) -> NewPixelColorEvent[RedisStreamOffset]:
        return NewPixelColorEvent(
            pixel=self.__raw_event_pixel_of(raw_event, chunk=chunk),
            offset=raw_event[0],
        )

    def __event_body_of(self, pixel: Pixel[RGBColor]) -> RedisStreamEventBody:
        return {bytes(0): encoded(pixel)}

    def __event_body_pixel_of(
        self, body: RedisStreamEventBody, *, chunk: Chunk
    ) -> Pixel[RGBColor]:
        encoded_pixel = body[bytes(0)]
        return decoded(encoded_pixel, chunk=chunk)

    def __raw_event_pixel_of(
        self, raw_event: RedisStreamEvent, *, chunk: Chunk
    ) -> Pixel[RGBColor]:
        return self.__event_body_pixel_of(raw_event[1], chunk=chunk)
