from pytest import fixture

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import black, white
from pixel_battle.entities.quantities.position import zero_position
from pixel_battle.infrastructure.adapters.pixels import InMemoryPixels


@fixture
def pixel1v() -> Pixel:
    return Pixel(position=zero_position, color=white)


@fixture
def pixel2v() -> Pixel:
    return Pixel(position=zero_position, color=black)


async def test_put_unstored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    pixels = InMemoryPixels([pixel2v])
    await pixels.put(pixel1v)

    assert set(pixels) == {pixel1v}


async def test_put_stored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    pixels = InMemoryPixels([pixel1v])

    await pixels.put(pixel2v)

    assert set(pixels) == {pixel2v}


async def test_remove_unstored_pixel(pixel1v: Pixel, pixel2v: Pixel) -> None:
    pixels = InMemoryPixels([pixel2v])
    await pixels.remove(pixel1v)

    assert set(pixels) == set()


async def test_remove_stored_pixel(pixel1v: Pixel) -> None:
    pixels = InMemoryPixels([pixel1v])
    await pixels.remove(pixel1v)

    assert set(pixels) == set()
