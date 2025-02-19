from abc import ABC, abstractmethod

from pixel_battle.application.ports.chunk_view import ChunkView


class ChunkViewFreezing[ChunkViewT: ChunkView, FrozenChunkViewT](ABC):
    @abstractmethod
    async def frozen(self, chunk_view: ChunkViewT) -> FrozenChunkViewT: ...
