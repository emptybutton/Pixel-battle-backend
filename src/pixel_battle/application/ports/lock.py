from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager


class Lock(ABC):
    @abstractmethod
    def __call__(self) -> AsyncContextManager[Any]: ...
