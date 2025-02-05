from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass

from pixel_battle.entities.core.chunk import Chunk


@dataclass(kw_only=True, frozen=True, slots=True)
class ActiveChunkOptimisticLock:
    is_owned: bool


type ChunkOptimisticLock = AbstractAsyncContextManager[ActiveChunkOptimisticLock]

# class ChunkOptimisticLock(
    
# ): ...


class ChunkOptimisticLockWhen(ABC):
    @abstractmethod
    def __call__(self, *, chunk: Chunk) -> ChunkOptimisticLock: ...
