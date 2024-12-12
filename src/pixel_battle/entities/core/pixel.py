from dataclasses import dataclass

from pixel_battle.entities.core.canvas import canvas
from pixel_battle.entities.core.chunk import Chunk, chunk_where
from pixel_battle.entities.core.user import (
    User,
    has_right_to_recolor,
    temporarily_without_right_to_recolor,
)
from pixel_battle.entities.quantities.color import (
    Color,
    RGBColor,
    white,
)
from pixel_battle.entities.quantities.position import Position
from pixel_battle.entities.quantities.time import Time


class PixelError(Exception): ...


class PixelOutOfCanvasError(PixelError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Pixel[ColorT: Color]:
    position: Position
    color: ColorT

    @property
    def chunk(self) -> Chunk:
        return chunk_where(self.position)

    def __post_init__(self) -> None:
        if self.position not in canvas.area:
            raise PixelOutOfCanvasError


def default_pixel_at(position: Position) -> Pixel[Color]:
    return Pixel(position=position, color=white)


def recolored[ColorT: Color](
    pixel: Pixel[ColorT], *, new_color: RGBColor
) -> Pixel[RGBColor]:
    return Pixel(position=pixel.position, color=new_color)


@dataclass(kw_only=True, frozen=True, slots=True)
class PixelRecoloringByUser:
    pixel: Pixel[RGBColor]
    user: User


class UserHasNoRightToRecolorError(Exception): ...


class UserInDifferentChunkToRecolorError(Exception): ...


def recolored_by[ColorT: Color](
    user: User,
    pixel: Pixel[ColorT],
    *,
    new_color: RGBColor,
    current_time: Time,
) -> PixelRecoloringByUser:
    if not has_right_to_recolor(user, current_time=current_time):
        raise UserHasNoRightToRecolorError

    if user.chunk != pixel.chunk:
        raise UserInDifferentChunkToRecolorError

    pixel = recolored(pixel, new_color=new_color)
    user = temporarily_without_right_to_recolor(user, current_time=current_time)

    return PixelRecoloringByUser(pixel=pixel, user=user)
