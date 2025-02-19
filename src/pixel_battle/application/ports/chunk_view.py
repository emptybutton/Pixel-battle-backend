from abc import ABC, abstractmethod
from collections.abc import Iterable
from types import TracebackType
from typing import Self

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


class ChunkView(ABC):
    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...

    @abstractmethod
    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        ...


class DefaultChunkViewWhen[ChunkViewT: ChunkView](ABC):
    @abstractmethod
    async def __call__(self, *, chunk: Chunk) -> ChunkViewT: ...
