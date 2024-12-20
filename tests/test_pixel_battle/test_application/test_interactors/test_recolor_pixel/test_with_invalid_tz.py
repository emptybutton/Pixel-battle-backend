from contextlib import suppress
from datetime import datetime

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.quantities.time import NotUTCTimeError


async def test_error(
    recolor_pixel: RecolorPixel
) -> None:
    with raises(NotUTCTimeError):
        await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime(2006, 1, 1),
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_broker(
    recolor_pixel: RecolorPixel
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime(2006, 1, 1),
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.broker
