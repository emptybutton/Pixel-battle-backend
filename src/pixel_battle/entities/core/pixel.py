from dataclasses import dataclass, field

from pixel_battle.entities.core.canvas import canvas
from pixel_battle.entities.core.chunk import Chunk, chunk_where
from pixel_battle.entities.core.pixel_battle import PixelBattle, is_going_on
from pixel_battle.entities.core.user import (
    User,
    has_recoloring_right,
    user_temporarily_without_recoloring_right_when,
)
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import Color, RGBColor
from pixel_battle.entities.space.time import Time


class PixelError(Exception): ...


class PixelOutOfCanvasError(PixelError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Pixel[ColorT: Color]:
    position: Vector
    color: ColorT

    @property
    def chunk(self) -> Chunk:
        return chunk_where(self.position)

    @property
    def position_within_chunk(self) -> Vector:
        return self.position - self.chunk.area.min_x_min_y_position

    def __post_init__(self) -> None:
        if self.position not in canvas.area:
            raise PixelOutOfCanvasError


def pixel_in(
    chunk: Chunk,
    *,
    position_within_chunk: Vector,
    color: RGBColor
) -> Pixel[RGBColor]:
    position = chunk.area.min_x_min_y_position + position_within_chunk

    return Pixel(color=color, position=position)


def recolored[ColorT: Color](
    pixel: Pixel[ColorT], *, new_color: RGBColor
) -> Pixel[RGBColor]:
    return Pixel(position=pixel.position, color=new_color)


@dataclass(kw_only=True, frozen=True, slots=True)
class RecoloredPixelByUser:
    pixel: Pixel[RGBColor] = field(kw_only=False)
    user: User


class UserHasNoRightToRecolorError(Exception): ...


class PixelBattleIsNotGoingOnToRecolorError(Exception): ...


def recolored_by_user[ColorT: Color](
    pixel: Pixel[ColorT],
    *,
    user: User,
    new_color: RGBColor,
    current_time: Time,
    pixel_battle: PixelBattle,
) -> RecoloredPixelByUser:
    if not is_going_on(pixel_battle, current_time=current_time):
        raise PixelBattleIsNotGoingOnToRecolorError

    if not has_recoloring_right(user, current_time=current_time):
        raise UserHasNoRightToRecolorError

    pixel = recolored(pixel, new_color=new_color)
    user = user_temporarily_without_recoloring_right_when(
        current_time=current_time
    )

    return RecoloredPixelByUser(pixel, user=user)
