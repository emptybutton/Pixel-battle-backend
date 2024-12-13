from dataclasses import dataclass, field
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
class ListChunkView(ChunkView):
    _pixel_by_position: dict[Position, Pixel[RGBColor]]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]] = tuple()) -> None:
        self._pixel_by_position = {pixel.position: pixel for pixel in pixels}

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(self._pixel_by_position.values())

    def __len__(self) -> int:
        return len(self._pixel_by_position)

    def __bool__(self) -> bool:
        return bool(self._pixel_by_position)

    async def redraw(self, pixel: Pixel[RGBColor]) -> None:
        self._pixel_by_position[pixel.position] = pixel


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryChunkViews[ChunkViewT: ChunkView](ChunkViews[ChunkViewT]):
    _view_by_chunk: dict[Chunk, ChunkViewT] = field(default_factory=dict)

    def to_dict(self) -> dict[Chunk, ChunkViewT]:
        return dict(self._view_by_chunk)

    async def chunk_view_of(self, chunk: Chunk) -> ChunkViewT | None:
        return self._view_by_chunk.get(chunk)

    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None:
        self._view_by_chunk[chunk] = view


class DefaultListChunkViewOf(DefaultChunkViewOf[ListChunkView]):
    async def __call__(self, _: Chunk) -> ListChunkView:
        return ListChunkView()
