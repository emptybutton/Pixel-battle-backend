from dataclasses import dataclass
from types import TracebackType
from typing import Self, Type

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.application.ports.transaction import (
    Transaction,
    TransactionOf,
)
from pixel_battle.infrastructure.adapters.chunk_view import InMemoryChunkViews


class ExitWithoutEnterError(Exception): ...


@dataclass(frozen=True, slots=True)
class InMemoryChunkViewsTransaction[ChunkViewT: ChunkView](Transaction):
    _views: InMemoryChunkViews[ChunkViewT]

    async def __aenter__(self) -> Self:
        self._views.begin()
        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if error is None:
            self._views.commit()
        else:
            self._views.rollback()

        return False


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryChunkViewsTransactionOf[ChunkViewT: ChunkView](
    TransactionOf[InMemoryChunkViews[ChunkViewT]]
):
    def __call__(
        self, chunk_views: InMemoryChunkViews[ChunkViewT]
    ) -> Transaction:
        return InMemoryChunkViewsTransaction(chunk_views)
