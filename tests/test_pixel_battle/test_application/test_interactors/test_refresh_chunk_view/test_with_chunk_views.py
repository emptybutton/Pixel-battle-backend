from pytest import fixture

from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


@fixture(autouse=True)
async def stored_data(
    refresh_chunk_view: RefreshChunkView[CollectionChunkView],
    chunk: Chunk,
    view1_2_and_2_1: CollectionChunkView,
) -> None:
    await refresh_chunk_view.chunk_views.put(view1_2_and_2_1, chunk=chunk)


async def test_chunk_views(
    refresh_chunk_view: RefreshChunkView[CollectionChunkView],
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
    chunk: Chunk,
) -> None:
    await refresh_chunk_view(0, 0)

    excepted_views = {chunk: CollectionChunkView([pixel1_2, pixel2_1])}

    assert dict(refresh_chunk_view.chunk_views) == excepted_views
