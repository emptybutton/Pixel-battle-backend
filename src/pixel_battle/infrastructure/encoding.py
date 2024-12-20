from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel, pixel_in
from pixel_battle.entities.quantities.color import RGBColor, RGBColorValue
from pixel_battle.entities.quantities.vector import Vector


def encoded(pixel: Pixel[RGBColor]) -> bytes:
    return bytes([
        pixel.position_within_chunk.x,
        pixel.position_within_chunk.y,
        pixel.color.red.number,
        pixel.color.green.number,
        pixel.color.blue.number,
    ])


def decoded(bytes_: bytes, *, chunk: Chunk) -> Pixel[RGBColor]:
    position_within_chunk = Vector(x=bytes_[0], y=bytes_[1])

    red = RGBColorValue(number=bytes_[2])
    green = RGBColorValue(number=bytes_[3])
    blue = RGBColorValue(number=bytes_[4])
    color = RGBColor(red=red, green=green, blue=blue)

    return pixel_in(
        chunk, position_within_chunk=position_within_chunk, color=color
    )
