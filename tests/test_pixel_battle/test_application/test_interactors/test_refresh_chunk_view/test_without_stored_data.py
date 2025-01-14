from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


async def test_chunk_views(
    refresh_chunk_view: RefreshChunkView[CollectionChunkView]
) -> None:
    await refresh_chunk_view(0, 0)

    views = dict(refresh_chunk_view.chunk_views)
    expected_views = {
        Chunk(number=ChunkNumber(x=0, y=0)): CollectionChunkView()
    }
    assert views == expected_views
