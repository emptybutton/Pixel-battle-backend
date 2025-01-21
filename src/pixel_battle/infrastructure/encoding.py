from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel, pixel_in
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, RGBColorValue


def encoded_pixel_when(*, pixel: Pixel[RGBColor]) -> bytes:
    return bytes([
        pixel.position_within_chunk.x,
        pixel.position_within_chunk.y,
        pixel.color.red_value.number,
        pixel.color.green_value.number,
        pixel.color.blue_value.number,
    ])


def decoded_pixel_when(
    *, encoded_pixel: bytes, chunk: Chunk
) -> Pixel[RGBColor]:
    position_within_chunk = Vector(x=encoded_pixel[0], y=encoded_pixel[1])

    red_value = RGBColorValue(number=encoded_pixel[2])
    green_value = RGBColorValue(number=encoded_pixel[3])
    blue_value = RGBColorValue(number=encoded_pixel[4])
    color = RGBColor(
        red_value=red_value, green_value=green_value, blue_value=blue_value
    )

    return pixel_in(
        chunk, position_within_chunk=position_within_chunk, color=color
    )


type ChunkData = tuple[int, int]


def encoded_chunk_when(*, chunk: Chunk) -> bytes:
    return bytes([chunk.number.x * 10 + chunk.number.y])


def encoded_chunk_from_data_when(*, chunk_data: ChunkData) -> bytes:
    x, y = chunk_data

    return bytes([x * 10 + y])


def decoded_chunk_when(*, encoded_chunk: bytes) -> Chunk:
    x, y = decoded_chunk_data_when(encoded_chunk=encoded_chunk)

    return Chunk(number=ChunkNumber(x=x, y=y))


def decoded_chunk_data_when(*, encoded_chunk: bytes) -> ChunkData:
    x = encoded_chunk[0] // 10
    y = encoded_chunk[0] - x * 10

    return x, y
