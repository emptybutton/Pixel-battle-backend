from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Self

from pixel_battle.application.ports.chunk_view import ChunkViews


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self


class TransactionOf[ChunkViewsT: ChunkViews[Any]](ABC):
    @abstractmethod
    def __call__(self, chunk_views: ChunkViewsT) -> Transaction: ...
