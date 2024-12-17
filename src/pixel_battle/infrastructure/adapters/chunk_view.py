from dataclasses import dataclass, field
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

    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        for pixel in pixels:
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


@dataclass(frozen=True, slots=True, eq=False, unsafe_hash=False)
class PNGImageChunkView(ChunkView):  # noqa: PLW1641
    _image: Image

    @classmethod
    def _image_size(cls) -> tuple[int, int]:
        size_vector = Chunk.size.to_vector() - Vector(x=1, y=1)

        return (size_vector.x, size_vector.y)

    def __post_init__(self) -> None:
        if self._image.mode != "RGB":
            raise InvalidPNGImageChunkViewModeError(self._image.mode)

        if self._image.size != PNGImageChunkView._image_size():
            raise InvalidPNGImageChunkViewSizeError(self._image.size)

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "PNGImageChunkView":
        image = open(BytesIO(bytes_), formats=["png"])

        return PNGImageChunkView(image)

    @classmethod
    def create_default(cls) -> "PNGImageChunkView":
        image = new(
            mode="RGB",
            size=PNGImageChunkView._image_size(),
            color=(255, 255, 255),
        )

        return PNGImageChunkView(image)

    def to_stream(self) -> BytesIO:
        stream = BytesIO()
        self._image.save(stream, format="png")

        return stream

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PNGImageChunkView):
            return False

        return self._image.tobytes() == other._image.tobytes()

    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        for pixel in pixels:
            coordinates = self.__coordinates_of(pixel)
            value = self.__value_of(pixel)

            self._image.putpixel(coordinates, value)

    def close(self) -> None:
        self._image.close()

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
        self.close()


class DefaultPNGImageChunkViewOf(DefaultChunkViewOf[PNGImageChunkView]):
    async def __call__(self, _: Chunk) -> PNGImageChunkView:
        return PNGImageChunkView.create_default()


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterPNGImageChunkViews(ChunkViews[PNGImageChunkView]):
    redis_cluster: RedisCluster
    close_when_putting: bool

    async def chunk_view_of(self, chunk: Chunk) -> PNGImageChunkView | None:
        raw_view = await self.redis_cluster.get(self.__key_by(chunk))

        if raw_view is None:
            return None

        return PNGImageChunkView.from_bytes(raw_view)

    async def put(self, view: PNGImageChunkView, *, chunk: Chunk) -> None:
        with view.to_stream() as stream:
            if self.close_when_putting:
                view.close()

            buffer = stream.getbuffer()
            await self.redis_cluster.set(self.__key_by(chunk), buffer)
            buffer.release()

    def __key_by(self, chunk: Chunk) -> bytes:
        return bytes([chunk.number.x, chunk.number.y]) + b"view"


@dataclass(frozen=True, slots=True)
class InMemoryChunkViews[ChunkViewT: ChunkView](ChunkViews[ChunkViewT]):
    _view_by_chunk: dict[Chunk, ChunkViewT] = field(default_factory=dict)

    def __bool__(self) -> bool:
        return bool(self._view_by_chunk)

    def to_dict(self) -> dict[Chunk, ChunkViewT]:
        return dict(self._view_by_chunk)

    async def chunk_view_of(self, chunk: Chunk) -> ChunkViewT | None:
        return self._view_by_chunk.get(chunk)

    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None:
        self._view_by_chunk[chunk] = view
