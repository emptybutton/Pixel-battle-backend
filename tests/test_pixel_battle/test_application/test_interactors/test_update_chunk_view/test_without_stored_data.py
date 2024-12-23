from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


async def test_offsets(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int]
) -> None:
    await update_chunk_view(0, 0)

    assert dict(update_chunk_view.offsets_of_latest_compressed_events) == dict()


async def test_chunk_views(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int]
) -> None:
    await update_chunk_view(0, 0)

    assert dict(update_chunk_view.chunk_views) == dict()
