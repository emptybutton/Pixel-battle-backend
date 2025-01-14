from contextlib import suppress

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.color import (
    RGBColorValueNumberInInvalidRangeError,
)


async def test_error_on_too_large_value_number(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=100_000_000,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_error_on_negative_value_number(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )


async def test_broker(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )

    assert not recolor_pixel.pixel_queue
