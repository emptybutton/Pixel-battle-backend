from contextlib import suppress
from datetime import UTC, datetime

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.quantities.color import (
    RGBColorValueNumberInInvalidRangeError,
)


async def test_error_on_too_large_value_number(
    recolor_pixel: RecolorPixel
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=100_000_000,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_error_on_negative_value_number(
    recolor_pixel: RecolorPixel
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )


async def test_broker(
    recolor_pixel: RecolorPixel
) -> None:
    with suppress(Exception):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )

    assert not recolor_pixel.broker
