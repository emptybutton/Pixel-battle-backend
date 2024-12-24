from pytest import fixture

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


@fixture(autouse=True)
async def stored_data(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
    view1_2_and_2_1: CollectionChunkView,
    pixel1_1: Pixel[RGBColor],
) -> None:
    await update_chunk_view.chunk_views.put(view1_2_and_2_1, chunk=chunk)
    await update_chunk_view.broker.push_new_event_with(pixel=pixel1_1)


async def test_offsets(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
) -> None:
    await update_chunk_view(0, 0)

    offsets = dict(update_chunk_view.offsets_of_latest_compressed_events)

    assert offsets == {chunk: 0}


async def test_chunk_views(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    pixel1_1: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
    chunk: Chunk,
) -> None:
    await update_chunk_view(0, 0)

    excepted_views = {chunk: CollectionChunkView([pixel1_1, pixel2_1])}

    assert dict(update_chunk_view.chunk_views) == excepted_views
