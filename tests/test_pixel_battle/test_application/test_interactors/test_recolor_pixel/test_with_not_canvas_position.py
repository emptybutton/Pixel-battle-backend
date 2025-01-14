from contextlib import suppress

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import PixelOutOfCanvasError
from pixel_battle.entities.core.user import User


async def test_error_on_too_large_x(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with raises(PixelOutOfCanvasError):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=16001,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_error_on_negative_x(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with raises(PixelOutOfCanvasError):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=-1,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_broker(
    recolor_pixel: RecolorPixel, input_signed_user_data: User
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=-1,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.pixel_queue
