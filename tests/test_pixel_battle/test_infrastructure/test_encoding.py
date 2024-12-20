from pytest import mark

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black, white
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.encoding import decoded, encoded


@mark.parametrize(
    "pixel",
    [
        Pixel(position=Vector(x=0, y=0), color=black),
        Pixel(position=Vector(x=99, y=99), color=white),
        Pixel(position=Vector(x=999, y=999), color=white),
    ],
)
def test_decoded_encoded(pixel: Pixel[RGBColor]) -> None:
    assert decoded(encoded(pixel), chunk=pixel.chunk) == pixel
