from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from pixel_battle.application.ports.pixels import Pixels
from pixel_battle.entities.color import color_with
from pixel_battle.entities.pixel import (
    Pixel,
    default_pixel_at,
    recolored_by,
)
from pixel_battle.entities.position import Position
from pixel_battle.entities.time import Time
from pixel_battle.entities.user import User, new_user_when


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user: User
    pixel: Pixel | None


@dataclass(kw_only=True, frozen=True, slots=True)
class RecolorPixel[PixelSetViewT]:
    pixels: Pixels[PixelSetViewT]

    async def __call__(
        self,
        user_id: UUID | None,
        datetime_of_user_obtaining_recoloring_right: datetime | None,
        pixel_position_x: int,
        pixel_position_y: int,
        new_color_red_value_number: int,
        new_color_green_value_number: int,
        new_color_blue_value_number: int,
    ) -> PixelSetViewT:
        current_time = Time(datetime=datetime.now(UTC))

        if None in {user_id, datetime_of_user_obtaining_recoloring_right}:
            user = new_user_when(current_time=current_time)
            return Output(user=user, pixel=None)

        user_time = Time(datetime=datetime_of_user_obtaining_recoloring_right)
        user = User(id=user_id, time_of_obtaining_recoloring_right=user_time)

        new_pixel_color = color_with(
            red_value_number=new_color_red_value_number,
            green_value_number=new_color_green_value_number,
            blue_value_number=new_color_blue_value_number,
        )

        pixel_position = Position(x=pixel_position_x, y=pixel_position_y)
        pixel = await self.pixels.pixel_at(pixel_position)

        default_pixel = default_pixel_at(pixel_position)

        if pixel is None:
            pixel = default_pixel

        result = recolored_by(
            user, pixel, new_color=new_pixel_color, current_time=current_time
        )

        if result.pixel == default_pixel:
            await self.pixels.remove(pixel)
        else:
            await self.pixels.update(result.pixel)

        return Output(user=user, pixel=pixel)
