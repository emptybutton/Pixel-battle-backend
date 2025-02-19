from abc import ABC, abstractmethod
from collections.abc import Sequence
from contextlib import AbstractAsyncContextManager
from enum import Enum, auto

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


class PullingProcess(Enum):
    chunk_view_refresh = auto()


type UncommittablePulledPixels = Sequence[Pixel[RGBColor]]
type CommittablePulledPixels = (
    AbstractAsyncContextManager[Sequence[Pixel[RGBColor]]]
)


class PixelQueue(ABC):
    @abstractmethod
    async def push(self, pixel: Pixel[RGBColor]) -> None: ...

    @abstractmethod
    def committable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None, only_new: bool
    ) -> CommittablePulledPixels: ...

    @abstractmethod
    async def uncommittable_pulled_pixels_when(
        self, *, chunk: Chunk, process: PullingProcess | None
    ) -> UncommittablePulledPixels: ...
