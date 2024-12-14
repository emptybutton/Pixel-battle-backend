from copy import deepcopy
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable, Iterator

from PIL.Image import Image, new, open
from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor
from pixel_battle.entities.quantities.vector import Vector


@dataclass(init=False)
class CollectionChunkView(ChunkView):
    _pixel_by_position: dict[Vector, Pixel[RGBColor]]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]] = tuple()) -> None:
        self._pixel_by_position = {pixel.position: pixel for pixel in pixels}

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(self._pixel_by_position.values())

    def __contains__(self, pixel: Pixel[RGBColor]) -> bool:
        return pixel in tuple(iter(self))

    def __len__(self) -> int:
        return len(self._pixel_by_position)

    def __bool__(self) -> bool:
        return bool(self._pixel_by_position)

    async def redraw(self, pixel: Pixel[RGBColor]) -> None:
        self._pixel_by_position[pixel.position] = pixel


class DefaultCollectionChunkViewOf(DefaultChunkViewOf[CollectionChunkView]):
    async def __call__(self, _: Chunk) -> CollectionChunkView:
        return CollectionChunkView()


class InvalidPNGImageChunkViewModeError(Exception):
    def __init__(self, mode: str) -> None:
        super().__init__(mode)


class InvalidPNGImageChunkViewSizeError(Exception):
    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)


@dataclass(frozen=True, slots=True)
class PNGImageChunkView(ChunkView):
    _image: Image

    def __post_init__(self) -> None:
        if self._image.mode != "PNG":
            raise InvalidPNGImageChunkViewModeError(self._image.mode)

        if self._image.size != (Chunk.width, Chunk.height):
            raise InvalidPNGImageChunkViewSizeError(self._image.size)

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "PNGImageChunkView":
        with BytesIO(bytes_) as stream:
            image = open(stream, formats=["png"])

            return PNGImageChunkView(image)

    def to_bytes(self) -> bytes:
        with BytesIO() as stream:
            self._image.save(stream, format="png")
            self._image.close()

            return stream.getvalue()

    async def redraw(self, pixel: Pixel[RGBColor]) -> None:
        coordinates = self.__coordinates_of(pixel)
        value = self.__value_of(pixel)

        self._image.putpixel(coordinates, value)

    def __coordinates_of(self, pixel: Pixel[RGBColor]) -> tuple[int, int]:
        position = pixel.position_within_chunk

        return (position.x, position.y)

    def __value_of(self, pixel: Pixel[RGBColor]) -> tuple[int, int, int]:
        return (
            pixel.color.red.number,
            pixel.color.green.number,
            pixel.color.blue.number,
        )

    def __del__(self) -> None:
        self._image.close()


class DefaultPNGImageChunkViewOf(DefaultChunkViewOf[PNGImageChunkView]):
    async def __call__(self, chunk: Chunk) -> PNGImageChunkView:
        image = new(
            mode="PNG",
            size=(chunk.width, chunk.height),
            color=(255, 255, 255),
        )

        return PNGImageChunkView(image)


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterPNGImageChunkViews(ChunkViews[PNGImageChunkView]):
    client: RedisCluster

    async def chunk_view_of(self, chunk: Chunk) -> PNGImageChunkView | None:
        raw_view = await self.client.get(self.__key_for(chunk))

        if raw_view is None:
            return None

        return PNGImageChunkView.from_bytes(raw_view)

    async def put(self, view: PNGImageChunkView, *, chunk: Chunk) -> None:
        await self.client.set(self.__key_for(chunk), view.to_bytes())

    def __key_for(self, chunk: Chunk) -> str:
        return f"{chunk.number.x}.{chunk.number.y}"


class NoTransactionError(Exception): ...


@dataclass(init=False)
class InMemoryChunkViews[ChunkViewT: ChunkView](ChunkViews[ChunkViewT]):
    _view_by_chunk: dict[Chunk, ChunkViewT]
    _snapshot: dict[Chunk, ChunkViewT] | None = None

    def __init__(self, view_by_chunk: dict[Chunk, ChunkViewT] = dict()) -> None:  # noqa: B006
        self._view_by_chunk = dict(view_by_chunk)

    def __bool__(self) -> bool:
        return bool(self._view_by_chunk)

    def to_dict(self) -> dict[Chunk, ChunkViewT]:
        return dict(self._view_by_chunk)

    def begin(self) -> None:
        self._snapshot = deepcopy(self._view_by_chunk)

    def rollback(self) -> None:
        if self._snapshot is None:
            raise NoTransactionError

        self._view_by_chunk = self._snapshot
        self._snapshot = None

    def commit(self) -> None:
        if self._snapshot is None:
            raise NoTransactionError

        self._snapshot = None

    async def chunk_view_of(self, chunk: Chunk) -> ChunkViewT | None:
        return self._view_by_chunk.get(chunk)

    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None:
        self._view_by_chunk[chunk] = view
