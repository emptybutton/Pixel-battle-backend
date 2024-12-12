from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black
from pixel_battle.entities.quantities.position import Position
from pixel_battle.infrastructure.adapters.pixels import (
    ChunkIdentityViewOfInMemoryPixels,
    InMemoryPixels,
)


@fixture
def chunk_view_of() -> ChunkIdentityViewOfInMemoryPixels:
    return ChunkIdentityViewOfInMemoryPixels()


async def test_without_pixels(
    chunk_view_of: ChunkIdentityViewOfInMemoryPixels
) -> None:
    chunk = Chunk(number=ChunkNumber(x=0, y=0))
    result = await chunk_view_of(InMemoryPixels(), chunk=chunk)

    assert result == frozenset()


@fixture
def chunk_0_pixeles() -> frozenset[Pixel[RGBColor]]:
    return frozenset([
        Pixel(position=Position(x=0, y=0), color=black),
        Pixel(position=Position(x=20, y=0), color=black),
        Pixel(position=Position(x=50, y=50), color=black),
    ])


@fixture
def chunk_1_pixeles() -> frozenset[Pixel[RGBColor]]:
    return frozenset([
        Pixel(position=Position(x=100, y=0), color=black),
        Pixel(position=Position(x=120, y=0), color=black),
        Pixel(position=Position(x=150, y=50), color=black),
    ])


@fixture
def chunk_0() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


async def test_with_pixels(
    chunk_view_of: ChunkIdentityViewOfInMemoryPixels,
    chunk_0_pixeles: frozenset[Pixel[RGBColor]],
    chunk_1_pixeles: frozenset[Pixel[RGBColor]],
    chunk_0: Chunk,
) -> None:
    pixels = InMemoryPixels(chunk_0_pixeles | chunk_1_pixeles)
    result = await chunk_view_of(pixels, chunk=chunk_0)

    assert result == chunk_0_pixeles
