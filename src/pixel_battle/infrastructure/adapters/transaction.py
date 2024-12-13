from dataclasses import dataclass
from types import TracebackType
from typing import ClassVar, Self, Type

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.application.ports.transaction import (
    Transaction,
    TransactionOf,
)
from pixel_battle.infrastructure.adapters.chunk_view import InMemoryChunkViews


@dataclass(init=False)
class InMemoryChunkViewsTransaction[ChunkViewT: ChunkView](
    Transaction
):
    _snapshot_views: InMemoryChunkViews[ChunkViewT] | None = None

    def __init__(self, views: InMemoryChunkViews[ChunkViewT]) -> None:
        self._views = views

    async def __aenter__(self) -> Self:
        self._snapshot_views = InMemoryChunkViews(self._views.to_dict())
        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if error is not None:
            self._views = self._snapshot_views

        self._snapshot_views = None

        return False


class InMemoryChunkViewsTransactionOf[ChunkViewT: ChunkView](
    TransactionOf[InMemoryChunkViews[ChunkViewT]]
):
    def __call__(
        self, chunk_views: InMemoryChunkViews[ChunkViewT]
    ) -> Transaction:
        return InMemoryChunkViewsTransaction(chunk_views)
