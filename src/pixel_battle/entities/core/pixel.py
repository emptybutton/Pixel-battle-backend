from dataclasses import dataclass

from pixel_battle.entities.core.canvas import canvas
from pixel_battle.entities.core.chunk import Chunk, chunk_where
from pixel_battle.entities.core.user import (
    User,
    has_right_to_recolor,
    temporarily_without_right_to_recolor,
)
from pixel_battle.entities.quantities.color import Color, RGBColor
from pixel_battle.entities.quantities.time import Time
from pixel_battle.entities.quantities.vector import Vector


class PixelError(Exception): ...


class PixelOutOfCanvasError(PixelError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Pixel[ColorT: Color]:
    position: Vector
    color: ColorT

    @property
    def id(self) -> Vector:
        return self.position

    @property
    def chunk(self) -> Chunk:
        return chunk_where(self.position)

    @property
    def position_within_chunk(self) -> Vector:
        return self.position - self.chunk.area.min_x_min_y_position

    def __post_init__(self) -> None:
        if self.position not in canvas.area:
            raise PixelOutOfCanvasError


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
