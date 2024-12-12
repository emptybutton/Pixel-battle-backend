from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black
from pixel_battle.entities.quantities.position import zero_position
from pixel_battle.infrastructure.adapters.pixels import InMemoryPixels


@fixture
def recolor_pixel() -> RecolorPixel[InMemoryPixels]:
    return RecolorPixel(
        chunk=Chunk(number=ChunkNumber(x=0, y=0)),
        pixels=InMemoryPixels(),
    )


@fixture
async def stored_pixel(
    recolor_pixel: RecolorPixel[InMemoryPixels]
) -> Pixel[RGBColor]:
    pixel = Pixel(position=zero_position, color=black)
    await recolor_pixel.pixels.put(pixel)

    return pixel
