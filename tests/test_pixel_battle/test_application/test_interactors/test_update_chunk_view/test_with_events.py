from pytest import fixture

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


@fixture(autouse=True)
async def stored_data(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    pixel1_1: Pixel[RGBColor],
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
) -> None:
    await update_chunk_view.broker.push_event_with(pixel=pixel1_1)
    await update_chunk_view.broker.push_event_with(pixel=pixel1_2)
    await update_chunk_view.broker.push_event_with(pixel=pixel2_1)


async def test_offsets(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
) -> None:
    await update_chunk_view(0, 0)

    offsets = dict(update_chunk_view.offsets_of_latest_compressed_events)

    assert offsets == {chunk: 2}


async def test_chunk_views(
    update_chunk_view: UpdateChunkView[CollectionChunkView, int],
    chunk: Chunk,
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
) -> None:
    await update_chunk_view(0, 0)

    views = dict(update_chunk_view.chunk_views)

    assert views == {chunk: CollectionChunkView([pixel1_2, pixel2_1])}
