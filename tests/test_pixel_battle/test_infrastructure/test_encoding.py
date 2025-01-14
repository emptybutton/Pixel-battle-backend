from pytest import mark

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, black, white
from pixel_battle.infrastructure.encoding import (
    decoded_pixel_when,
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
def test_decoded_encoded(pixel: Pixel[RGBColor]) -> None:
    result_pixel = decoded_pixel_when(
        encoded_pixel=encoded_pixel_when(pixel=pixel),
        chunk=pixel.chunk
    )

    assert result_pixel == pixel
