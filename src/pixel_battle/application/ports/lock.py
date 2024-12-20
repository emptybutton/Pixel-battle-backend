from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager

from pixel_battle.entities.core.chunk import Chunk


class Lock(ABC):
    @abstractmethod
    def __call__(self, chunk: Chunk) -> AsyncContextManager[Any]: ...
