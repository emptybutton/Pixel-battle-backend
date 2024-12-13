from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Self

from pixel_battle.application.ports.chunk_view import ChunkView, ChunkViews


class Transaction(AbstractAsyncContextManager["Transaction"]):
    async def __aenter__(self) -> Self:
        return self


class TransactionOf[ChunkViewsT: ChunkViews[ChunkView]](ABC):
    @abstractmethod
    def __call__(self, chunk_views: ChunkViewsT) -> Transaction: ...
