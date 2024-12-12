from contextlib import suppress
from datetime import UTC, datetime
from uuid import uuid4

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import PixelOutOfCanvasError
from pixel_battle.infrastructure.adapters.pixels import InMemoryPixels


async def test_error_on_too_large_x(
    recolor_pixel: RecolorPixel[InMemoryPixels]
) -> None:
    with raises(PixelOutOfCanvasError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=16001,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_error_on_negative_x(
    recolor_pixel: RecolorPixel[InMemoryPixels]
) -> None:
    with raises(PixelOutOfCanvasError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=-1,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_stored_pixels(
    recolor_pixel: RecolorPixel[InMemoryPixels]
) -> None:
    with suppress(Exception):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=-1,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.pixels
