from abc import ABC, abstractmethod

from pixel_battle.entities.core.chunk import Chunk


class Offsets[OffsetT](ABC):
    @abstractmethod
    async def put(self, offset: OffsetT, *, chunk: Chunk) -> None: ...

    @abstractmethod
    async def offset_for(self, chunk: Chunk) -> OffsetT | None: ...
