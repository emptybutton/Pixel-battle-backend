from pixel_battle.entities.core.chunk import Chunk
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
