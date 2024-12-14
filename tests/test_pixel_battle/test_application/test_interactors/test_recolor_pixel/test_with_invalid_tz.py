from contextlib import suppress
from datetime import datetime
from uuid import uuid4

from pytest import raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.quantities.time import NotUTCTimeError
from pixel_battle.infrastructure.adapters.chunk_view import CollectionChunkView


async def test_error(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    with raises(NotUTCTimeError):
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime(2006, 1, 1),
            pixel_position_x=0,
            pixel_position_y=0,
            chunk_number_x=0,
            chunk_number_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_chunk_views(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            user_id=uuid4(),
            datetime_of_user_obtaining_recoloring_right=datetime(2006, 1, 1),
            pixel_position_x=0,
            pixel_position_y=0,
            chunk_number_x=0,
            chunk_number_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.chunk_views
