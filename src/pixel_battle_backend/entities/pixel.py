from dataclasses import dataclass

from pixel_battle_backend.entities.color import Color, white
from pixel_battle_backend.entities.position import Position
from pixel_battle_backend.entities.time import Time
from pixel_battle_backend.entities.user import (
    User,
    has_right_to_recolor,
    temporarily_without_right_to_recolor,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Pixel:
    position: Position
    color: Color


def default_pixel_at(position: Position) -> Pixel:
    return Pixel(position=position, color=white)


def recolored(pixel: Pixel, *, new_color: Color) -> Pixel:
    return Pixel(position=pixel.position, color=new_color)


@dataclass(kw_only=True, frozen=True, slots=True)
class PixelRecoloringByUser:
    pixel: Pixel
    user: User


class UserHasNoRightToRecolorError(Exception): ...


def recolored_by(
    user: User,
    pixel: Pixel,
    *,
    new_color: Color,
    current_time: Time,
) -> PixelRecoloringByUser:
    if not has_right_to_recolor(user):
        raise UserHasNoRightToRecolorError

    pixel = recolored(pixel, new_color=new_color)
    user = temporarily_without_right_to_recolor(user, current_time=current_time)

    return PixelRecoloringByUser(pixel=pixel, user=user)
