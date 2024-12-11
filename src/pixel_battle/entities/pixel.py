from dataclasses import dataclass
from functools import cached_property

from pixel_battle.entities.chunk import Chunk, chunk_where
from pixel_battle.entities.color import (
    Color,
    RGBColor,
    white,
)
from pixel_battle.entities.map import map_
from pixel_battle.entities.position import Position
from pixel_battle.entities.time import Time
from pixel_battle.entities.user import (
    User,
    has_right_to_recolor,
    temporarily_without_right_to_recolor,
)


class PixelError(Exception): ...


class PixelOutOfMapError(PixelError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Pixel[ColorT: Color]:
    position: Position
    color: ColorT

    @cached_property
    def chunk(self) -> Chunk:
        return chunk_where(self.position)

    def __post_init__(self) -> None:
        if self.position not in map_:
            raise PixelOutOfMapError


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


class UserInDifferentChunkError(Exception): ...


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
        raise UserInDifferentChunkError

    pixel = recolored(pixel, new_color=new_color)
    user = temporarily_without_right_to_recolor(user, current_time=current_time)

    return PixelRecoloringByUser(pixel=pixel, user=user)
