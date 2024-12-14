from pytest import fixture

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import black, white
from pixel_battle.entities.quantities.position import zero_position
from pixel_battle.infrastructure.adapters.chunk_view import CollectionChunkView


@fixture
def pixel1v() -> Pixel:
    return Pixel(position=zero_position, color=white)


@fixture
def pixel2v() -> Pixel:
    return Pixel(position=zero_position, color=black)


async def test_redraw_unstored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    view = CollectionChunkView([pixel2v])
    await view.redraw(pixel1v)

    assert set(view) == {pixel1v}


async def test_put_stored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    view = CollectionChunkView([pixel1v])
    await view.redraw(pixel2v)

    assert set(view) == {pixel2v}
