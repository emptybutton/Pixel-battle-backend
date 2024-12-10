from dataclasses import dataclass

from pixel_battle_backend.application.ports.pixels import Pixels
from pixel_battle_backend.application.ports.position import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewPixelsInsideRectangle[PixelSetViewT]:
    pixels: Pixels[PixelSetViewT]

    async def __call__(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> PixelSetViewT:
        position1 = Position(x=x1, y=y1)
        position2 = Position(x=x2, y=y2)

        view = self.pixels.view_of_pixels_inside_rectangle(position1, position2)
        return await view
