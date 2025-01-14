from asyncio import sleep
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import (
    AsyncIterator,
    Iterable,
    Iterator,
    Sequence,
)

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.lock import Lock as _RedisLock

from pixel_battle.application.ports.pixel_queue import (
    PixelQueue,
    PullingProcess,
    UncommittablePulledPixels,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.encoding import (
    decoded_pixel_when,
    encoded_pixel_when,
)
from pixel_battle.infrastructure.redis.keys import chunk_key_when
from pixel_battle.infrastructure.redis.types import (
    RedisStreamEvent,
    RedisStreamKey,
    RedisStreamOffset,
    RedisStreamResults,
)
from pixel_battle.infrastructure.types import Index


@dataclass(init=False)
class InMemoryPixelQueue(PixelQueue):
    __pixels_by_chunk: defaultdict[Chunk, list[Pixel[RGBColor]]]
    __uncommited_pixel_index_by_chunk_and_process: dict[
        tuple[Chunk, PullingProcess | None], Index
    ]
    __pulling_timeout_seconds: int | float

    def __init__(
        self,
        pixels: Iterable[Pixel[RGBColor]] = tuple(),
        *,
        pulling_timeout_seconds: int | float,
    ) -> None:
        self.__pixels_by_chunk = defaultdict(list)
        self.__pulling_timeout_seconds = pulling_timeout_seconds
        self.__uncommited_pixel_index_by_chunk_and_process = dict()

        for pixel in pixels:
            self.__pixels_by_chunk[pixel.chunk].append(pixel)

    def __iter__(self) -> Iterator[tuple[Chunk, list[Pixel[RGBColor]]]]:
        return iter(tuple(
            (chunk, list(pixels))
            for chunk, pixels in self.__pixels_by_chunk.items()
        ))

    def __bool__(self) -> bool:
        return bool(self.__pixels_by_chunk)

    async def push(self, pixel: Pixel[RGBColor]) -> None:
        self.__pixels_by_chunk[pixel.chunk].append(pixel)

    @asynccontextmanager
    async def committable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None, only_new: bool
    ) -> AsyncIterator[tuple[Pixel[RGBColor], ...]]:
        yield await self.__pull(
            chunk,
            process,
            only_new=only_new,
            and_commit=True,
        )

    async def uncommittable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None, only_new: bool
    ) -> tuple[Pixel[RGBColor], ...]:
        return await self.__pull(
            chunk,
            process,
            only_new=only_new,
            and_commit=False,
        )

    async def __pull(
        self,
        chunk: Chunk,
        process: PullingProcess | None,
        *,
        only_new: bool,
        and_commit: bool,
    ) -> tuple[Pixel[RGBColor], ...]:
        chunk_and_process = chunk, process
        uncommited_pixel_index = (
            self.__uncommited_pixel_index_by_chunk_and_process
            .get(chunk_and_process)
        )

        if uncommited_pixel_index is None:
            if only_new:
                uncommited_pixel_index = len(self.__pixels_by_chunk[chunk])
            else:
                uncommited_pixel_index = 0

        if len(self.__pixels_by_chunk[chunk]) == uncommited_pixel_index:
            await sleep(self.__pulling_timeout_seconds)

        pulled_pixels = self.__pixels_by_chunk[chunk][uncommited_pixel_index:]

        if and_commit:
            new_uncommited_pixel_index = (
                uncommited_pixel_index + len(pulled_pixels)
            )
            self.__uncommited_pixel_index_by_chunk_and_process[chunk_and_process] = (  # noqa: E501
                new_uncommited_pixel_index
            )

        return tuple(pulled_pixels)


class InvalidPullingProcessError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisClusterStreamPixelQueue(PixelQueue):
    redis_cluster: RedisCluster
    max_stream_lenght: int = 5_000_000
    pulling_timeout_seconds: int | float = 3
    lock_timeout_seconds: int | float = 5
    lock_blocking_timeout_seconds: int | float = 15
    last_readed_event_offset_by_chunk: dict[Chunk, RedisStreamOffset] = (
        field(default_factory=dict)
    )

    async def push(self, pixel: Pixel[RGBColor]) -> None:
        key = self.__stream_key_when(chunk=pixel.chunk)
        event_body = {bytes(0): encoded_pixel_when(pixel=pixel)}

        maxlen = self.max_stream_lenght
        await self.redis_cluster.xadd(key, event_body, maxlen=maxlen)  # type: ignore[arg-type]

    async def uncommittable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None, only_new: bool
    ) -> UncommittablePulledPixels:
        key = self.__stream_key_when(chunk=chunk)
        offset = await self.__offset_when(
            chunk=chunk, process=process, only_new=only_new
        )
        results = await self.__pull(key=key, offset=offset)

        return self.__pixels_when(results=results, chunk=chunk)

    @asynccontextmanager
    async def committable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None, only_new: bool
    ) -> AsyncIterator[Sequence[Pixel[RGBColor]]]:
        async with self.__lock(chunk):
            key = self.__stream_key_when(chunk=chunk)
            offset = await self.__offset_when(
                chunk=chunk, process=process, only_new=only_new
            )
            results = await self.__pull(key=key, offset=offset)

            yield self.__pixels_when(results=results, chunk=chunk)

            await self.__commit_offset(
                process=process, chunk=chunk, results=results
            )

    async def __pull(
        self, *, key: RedisStreamKey, offset: RedisStreamOffset
    ) -> RedisStreamResults:
        block = int(self.pulling_timeout_seconds * 1000)
        return await self.redis_cluster.xread({key: offset}, block=block)

    def __lock(self, chunk: Chunk) -> _RedisLock:
        return _RedisLock(
            name=chunk_key_when(chunk=chunk) + b"lock",
            redis=self.redis_cluster,
            timeout=self.lock_timeout_seconds,
            blocking_timeout=self.lock_blocking_timeout_seconds,
            thread_local=False,
        )

    def __stream_key_when(self, *, chunk: Chunk) -> bytes:
        return chunk_key_when(chunk=chunk) + b"stream"

    def __offset_key_when(self, *, chunk: Chunk) -> bytes:
        return chunk_key_when(chunk=chunk)

    def __offset_field_when(
        self, *, process: PullingProcess
    ) -> RedisStreamOffset:
        base = b"offset"

        match process:
            case PullingProcess.chunk_view_refresh:
                return base + bytes([0])
            case _:
                raise InvalidPullingProcessError

    def __pixels_when(
        self, *, results: RedisStreamResults, chunk: Chunk
    ) -> tuple[Pixel[RGBColor], ...]:
        if not results:
            return tuple()

        result = results[0]
        _, events = result

        return tuple(
            self.__pixel_when(event=event, chunk=chunk)
            for event in events
        )

    def __pixel_when(
        self, *, event: RedisStreamEvent, chunk: Chunk
    ) -> Pixel[RGBColor]:
        event_body = event[1]
        encoded_pixel = event_body[bytes(0)]

        return decoded_pixel_when(encoded_pixel=encoded_pixel, chunk=chunk)

    async def __offset_when(
        self,
        *,
        process: PullingProcess | None,
        only_new: bool,
        chunk: Chunk,
    ) -> RedisStreamOffset:
        default_offset = self.__default_offset_when(only_new=only_new)

        if process is None:
            offset = self.last_readed_event_offset_by_chunk.get(chunk)
            return offset or default_offset

        key = self.__offset_key_when(chunk=chunk)
        offset_field = self.__offset_field_when(process=process)
        offset: bytes | None = await self.redis_cluster.hget(key, offset_field)  # type: ignore[misc, arg-type, no-redef]

        return offset or default_offset

    async def __commit_offset(
        self,
        *,
        process: PullingProcess | None,
        chunk: Chunk,
        results: RedisStreamResults,
    ) -> None:
        last_readed_event_offset = results[0][1][-1][0]

        if process is None:
            self.last_readed_event_offset_by_chunk[chunk] = (
                last_readed_event_offset
            )
            return

        key = self.__offset_key_when(chunk=chunk)
        offset_field = self.__offset_field_when(process=process)

        await self.redis_cluster.hset(
            key, offset_field, last_readed_event_offset
        )  # type: ignore[misc, arg-type]

    def __default_offset_when(self, *, only_new: bool) -> RedisStreamOffset:
        return b"$" if only_new else b"0"
