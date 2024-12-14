from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewOf,
)


async def test_result() -> None:
    view_of = DefaultCollectionChunkViewOf()
    view = await view_of(Chunk(number=ChunkNumber(x=0, y=0)))

    assert view == CollectionChunkView()
