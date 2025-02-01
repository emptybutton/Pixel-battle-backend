from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, black, white
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewWhen,
)


@fixture
def pixel1v() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=white)


@fixture
def pixel2v() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=black)


async def test_redraw_by_unstored_pixel(
    pixel1v: Pixel[RGBColor], pixel2v: Pixel[RGBColor]
) -> None:
    view = CollectionChunkView([pixel2v])
    await view.redraw_by_pixels([pixel1v])

    assert set(view) == {pixel1v}


async def test_put_stored_pixel(
    pixel1v: Pixel[RGBColor], pixel2v: Pixel[RGBColor]
) -> None:
    view = CollectionChunkView([pixel1v])
    await view.redraw_by_pixels([pixel2v])

    assert set(view) == {pixel2v}


async def test_default_collection_chunk_view_when() -> None:
    chunk_view_when = DefaultCollectionChunkViewWhen()

    chunk = Chunk(number=ChunkNumber(x=0, y=0))
    chunk_view = await chunk_view_when(chunk=chunk)

    assert chunk_view == CollectionChunkView()
