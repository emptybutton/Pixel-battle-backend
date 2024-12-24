from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from pixel_battle.application.ports.broker import Broker
from pixel_battle.entities.core.pixel import Pixel, recolored_by
from pixel_battle.entities.core.user import (
    User,
    user_temporarily_without_recoloring_right_when,
)
from pixel_battle.entities.quantities.color import (
    RGBColor,
    RGBColorValue,
    unknown_color,
)
from pixel_battle.entities.quantities.time import Time
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user: User
    pixel: Pixel[RGBColor] | None


@dataclass(kw_only=True, frozen=True, slots=True)
class RecolorPixel:
    broker: Broker[Any]

    async def __call__(
        self,
        datetime_of_obtaining_recoloring_right: datetime | None,
        pixel_position_x: int,
        pixel_position_y: int,
        new_color_red_value_number: int,
        new_color_green_value_number: int,
        new_color_blue_value_number: int,
    ) -> Output:
        current_time = Time(datetime=datetime.now(UTC))

        if datetime_of_obtaining_recoloring_right is None:
            user = user_temporarily_without_recoloring_right_when(
                current_time=current_time
            )
            return Output(user=user, pixel=None)

        time = Time(datetime=datetime_of_obtaining_recoloring_right)
        user = User(time_of_obtaining_recoloring_right=time)

        pixel_position = Vector(x=pixel_position_x, y=pixel_position_y)
        pixel = Pixel(position=pixel_position, color=unknown_color)

        new_pixel_color = RGBColor(
            red=RGBColorValue(number=new_color_red_value_number),
            green=RGBColorValue(number=new_color_green_value_number),
            blue=RGBColorValue(number=new_color_blue_value_number),
        )

        result = recolored_by(
            user,
            pixel,
            new_color=new_pixel_color,
            current_time=current_time,
        )

        await self.broker.push_new_event_with(pixel=result.pixel)

        return Output(user=result.user, pixel=result.pixel)
