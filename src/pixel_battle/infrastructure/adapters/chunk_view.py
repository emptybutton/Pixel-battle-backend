from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable, Iterator

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor
from pixel_battle.entities.quantities.position import Position


@dataclass(init=False)
class CollectionChunkView(ChunkView):
    _pixel_by_position: dict[Position, Pixel[RGBColor]]

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
