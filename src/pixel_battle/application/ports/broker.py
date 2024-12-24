from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncContextManager, Sequence

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class NewPixelColorEvent[OffsetT]:
    offset: OffsetT
    pixel: Pixel[RGBColor]


class Broker[OffsetT](ABC):
    @abstractmethod
    async def push_new_event_with(self, *, pixel: Pixel[RGBColor]) -> None: ...

    @abstractmethod
    async def events_after(
        self, offset: OffsetT, *, chunk: Chunk
    ) -> Sequence[NewPixelColorEvent[OffsetT]]:
        ...

    @abstractmethod
    async def all_events_where(
        self, *, chunk: Chunk
    ) -> Sequence[NewPixelColorEvent[OffsetT]]: ...

    @abstractmethod
    def pulled_events_where(
        self, *, chunk: Chunk
    ) -> AsyncContextManager[Sequence[NewPixelColorEvent[OffsetT]]]:
        ...
