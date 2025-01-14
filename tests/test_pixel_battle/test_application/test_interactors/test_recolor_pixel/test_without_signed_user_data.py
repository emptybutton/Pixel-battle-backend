from pixel_battle.application.interactors.recolor_pixel import (
    Output,
    RecolorPixel,
)
from pixel_battle.entities.core.user import User


async def test_result(
    recolor_pixel: RecolorPixel,
    output_signed_user_data: User,
) -> None:
    output = await recolor_pixel(
        signed_user_data=None,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    expected_result = Output(
        pixel=None, signed_user_data=output_signed_user_data
    )

    assert output == expected_result


async def test_broker(
    recolor_pixel: RecolorPixel
) -> None:
    await recolor_pixel(
        signed_user_data=None,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert not recolor_pixel.pixel_queue
