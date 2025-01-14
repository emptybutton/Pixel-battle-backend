from dataclasses import dataclass

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.pixel import Pixel, recolored_by_user
from pixel_battle.entities.core.user import (
    user_temporarily_without_recoloring_right_when,
)
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    RGBColor,
    RGBColorValue,
    unknown_color,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[SignedUserDataT]:
    signed_user_data: SignedUserDataT
    pixel: Pixel[RGBColor] | None


@dataclass(kw_only=True, frozen=True, slots=True)
class RecolorPixel[SignedUserDataT]:
    pixel_queue: PixelQueue
    user_data_signing: UserDataSigning[SignedUserDataT]
    clock: Clock

    async def __call__(
        self,
        signed_user_data: SignedUserDataT | None,
        pixel_position_x: int,
        pixel_position_y: int,
        new_color_red_value_number: int,
        new_color_green_value_number: int,
        new_color_blue_value_number: int,
    ) -> Output[SignedUserDataT]:
        current_time = await self.clock.get_current_time()

        if signed_user_data is not None:
            user = await self.user_data_signing.user_when(
                signed_user_data=signed_user_data
            )
        else:
            user = None

        if user is None:
            user = user_temporarily_without_recoloring_right_when(
                current_time=current_time
            )
            signed_user_data = await (
                self.user_data_signing.signed_user_data_when(user=user)
            )
            return Output(signed_user_data=signed_user_data, pixel=None)

        pixel_position = Vector(x=pixel_position_x, y=pixel_position_y)
        pixel = Pixel(position=pixel_position, color=unknown_color)

        new_pixel_color = RGBColor(
            red_value=RGBColorValue(number=new_color_red_value_number),
            green_value=RGBColorValue(number=new_color_green_value_number),
            blue_value=RGBColorValue(number=new_color_blue_value_number),
        )

        result = recolored_by_user(
            pixel,
            user=user,
            new_color=new_pixel_color,
            current_time=current_time,
        )

        await self.pixel_queue.push(result.pixel)

        signed_user_data = await self.user_data_signing.signed_user_data_when(
            user=result.user
        )
        return Output(signed_user_data=signed_user_data, pixel=result.pixel)
