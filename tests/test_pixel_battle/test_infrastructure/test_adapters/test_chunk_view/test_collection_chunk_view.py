from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import black, white
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewOf,
)


@fixture
def pixel1v() -> Pixel:
    return Pixel(position=Vector(), color=white)


@fixture
def pixel2v() -> Pixel:
    return Pixel(position=Vector(), color=black)


async def test_redraw_by_unstored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    view = CollectionChunkView([pixel2v])
    await view.redraw_by_pixels([pixel1v])

    assert set(view) == {pixel1v}


async def test_put_stored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    view = CollectionChunkView([pixel1v])
    await view.redraw_by_pixels([pixel2v])

    assert set(view) == {pixel2v}


async def test_default_of() -> None:
    view_of = DefaultCollectionChunkViewOf()
    view = await view_of(Chunk(number=ChunkNumber(x=0, y=0)))

    assert view == CollectionChunkView()
