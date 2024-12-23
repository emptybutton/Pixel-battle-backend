from pytest import fixture

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


@fixture(autouse=True)
async def stored_data(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
) -> None:
    offsets = update_chunk_view.offsets_of_latest_compressed_events
    await offsets.put(5, chunk=chunk)


async def test_offsets(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
) -> None:
    await update_chunk_view(0, 0)

    offsets = dict(update_chunk_view.offsets_of_latest_compressed_events)

    assert offsets == {chunk: 5}


async def test_chunk_views(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
) -> None:
    await update_chunk_view(0, 0)

    views = dict(update_chunk_view.chunk_views)

    assert views == dict()
