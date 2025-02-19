from abc import ABC, abstractmethod

from pixel_battle.entities.core.chunk import Chunk


class FrozenChunkViews[FrozenChunkViewT](ABC):
    @abstractmethod
    async def frozen_chunk_view_when(
        self, *, chunk: Chunk
    ) -> FrozenChunkViewT | None: ...

    @abstractmethod
    async def put(self, view: FrozenChunkViewT, *, chunk: Chunk) -> None: ...
