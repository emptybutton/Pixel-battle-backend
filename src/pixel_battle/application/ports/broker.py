from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, Sequence

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class NewPixelStateEvent:
    offset: int
    pixel: Pixel[RGBColor]


class Broker(ABC):
    @abstractmethod
    async def publish_event_with(self, *, pixel: Pixel[RGBColor]) -> None: ...

    @abstractmethod
    async def events_from(
        self, offset: int, * chunk: Chunk
    ) -> Sequence[NewPixelStateEvent]:
        ...

    @abstractmethod
    def new_events_of(
        self, chunk: Chunk
    ) -> AsyncContextManager[Sequence[NewPixelStateEvent]]:
        ...
