from abc import ABC, abstractmethod

from pixel_battle.entities.core.chunk import Chunk


class Offsets(ABC):
    @abstractmethod
    async def put(self, offset: int, *, chunk: Chunk) -> None: ...

    @abstractmethod
    async def offset_for(self, chunk: Chunk) -> int | None: ...
