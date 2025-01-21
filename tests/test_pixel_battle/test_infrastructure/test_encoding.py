from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, black, white
from pixel_battle.infrastructure.encoding import (
    ChunkData,
    decoded_chunk_data_when,
    decoded_chunk_when,
    decoded_pixel_when,
    encoded_chunk_from_data_when,
    encoded_chunk_when,
    encoded_pixel_when,
)


@mark.parametrize(
    "pixel",
    [
        Pixel(position=Vector(x=0, y=0), color=black),
        Pixel(position=Vector(x=99, y=99), color=white),
        Pixel(position=Vector(x=999, y=999), color=white),
    ],
)
def test_decoded_encoded_pixel(pixel: Pixel[RGBColor]) -> None:
    result_pixel = decoded_pixel_when(
        encoded_pixel=encoded_pixel_when(pixel=pixel),
        chunk=pixel.chunk
    )

    assert result_pixel == pixel


@mark.parametrize(
    "chunk",
    [
        Chunk(number=ChunkNumber(x=0, y=0)),
        Chunk(number=ChunkNumber(x=9, y=0)),
        Chunk(number=ChunkNumber(x=0, y=9)),
        Chunk(number=ChunkNumber(x=9, y=9)),
    ],
)
def test_decoded_encoded_chunk(chunk: Chunk) -> None:
    encoded_chunk = encoded_chunk_when(chunk=chunk)
    result_chunk = decoded_chunk_when(encoded_chunk=encoded_chunk)

    assert result_chunk == chunk


@mark.parametrize("chunk_data", [(0, 0), (9, 0), (0, 9), (9, 9)])
def test_decoded_encoded_chunk_data(chunk_data: ChunkData) -> None:
    encoded_chunk = encoded_chunk_from_data_when(chunk_data=chunk_data)
    result_chunk_data = decoded_chunk_data_when(encoded_chunk=encoded_chunk)

    assert result_chunk_data == chunk_data
