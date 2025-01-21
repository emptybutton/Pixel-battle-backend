from contextlib import suppress

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import (
    InvalidSignedUserDataError,
    RecolorPixel,
)


async def test_result(recolor_pixel: RecolorPixel) -> None:
    with raises(InvalidSignedUserDataError):
        await recolor_pixel(
            signed_user_data=None,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_pixel_queue(
    recolor_pixel: RecolorPixel
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            signed_user_data=None,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.pixel_queue
