from abc import ABC, abstractmethod

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.entities.core.chunk import Chunk


class ChunkViews[ChunkViewT: ChunkView](ABC):
    @abstractmethod
    async def chunk_view_where(self, *, chunk: Chunk) -> ChunkViewT | None: ...

    @abstractmethod
    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None: ...
