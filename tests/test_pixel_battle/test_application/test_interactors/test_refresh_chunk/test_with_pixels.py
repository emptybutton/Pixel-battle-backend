from pytest import fixture

from pixel_battle.application.interactors.refresh_chunk import (
    RefreshChunk,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
)


@fixture(autouse=True)
async def stored_data(
    refresh_chunk: RefreshChunk[CollectionChunkView],
    pixel1_1: Pixel[RGBColor],
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
) -> None:
    await refresh_chunk.pixel_queue.push(pixel1_1)
    await refresh_chunk.pixel_queue.push(pixel1_2)
    await refresh_chunk.pixel_queue.push(pixel2_1)


async def test_chunk_views(
    refresh_chunk: RefreshChunk[CollectionChunkView],
    chunk: Chunk,
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
) -> None:
    await refresh_chunk(0, 0)

    views = dict(refresh_chunk.chunk_views)  # type: ignore[call-overload]

    assert views == {chunk: CollectionChunkView([pixel1_2, pixel2_1])}
