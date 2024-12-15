from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any

from pixel_battle.entities.core.chunk import Chunk


class Lock(ABC):
    @abstractmethod
    def __call__(self, chunk: Chunk) -> AbstractAsyncContextManager[Any]: ...
