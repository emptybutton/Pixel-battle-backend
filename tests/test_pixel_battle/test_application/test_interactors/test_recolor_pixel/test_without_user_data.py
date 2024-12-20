from pixel_battle.application.interactors.recolor_pixel import RecolorPixel


async def test_result(
    recolor_pixel: RecolorPixel
) -> None:
    output = await recolor_pixel(
        datetime_of_obtaining_recoloring_right=None,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert output.pixel is None


async def test_broker(
    recolor_pixel: RecolorPixel
) -> None:
    await recolor_pixel(
        datetime_of_obtaining_recoloring_right=None,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert not recolor_pixel.broker
