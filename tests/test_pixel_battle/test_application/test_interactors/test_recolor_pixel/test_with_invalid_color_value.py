from contextlib import suppress
from datetime import UTC, datetime
from uuid import uuid4

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.quantities.color import (
    RGBColorValueNumberInInvalidRangeError,
)
from pixel_battle.infrastructure.adapters.chunk_view import CollectionChunkView


async def test_error_on_too_large_value_number(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            chunk_number_x=0,
            chunk_number_y=0,
            new_color_red_value_number=100_000_000,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_error_on_negative_value_number(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            chunk_number_x=0,
            chunk_number_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )


async def test_chunk_views(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    with suppress(Exception):
        datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime_,
            pixel_position_x=0,
            pixel_position_y=0,
            chunk_number_x=0,
            chunk_number_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=-1,
        )

    assert not recolor_pixel.chunk_views
