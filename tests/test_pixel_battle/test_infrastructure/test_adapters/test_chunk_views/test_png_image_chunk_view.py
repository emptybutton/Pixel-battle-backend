from pytest import mark

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import blue
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView


@mark.parametrize(
    "position",
    [Vector(x=2, y=1), Vector(x=102, y=101), Vector(x=102, y=1)],
)
async def test_redraw(
    position: Vector, png_image_chunk_view1: PNGImageChunkView
) -> None:
    pixel = Pixel(position=position, color=blue)

    png_image_chunk_view1_mimic = PNGImageChunkView.create_default()
    await png_image_chunk_view1_mimic.redraw(pixel)

    assert png_image_chunk_view1_mimic == png_image_chunk_view1
