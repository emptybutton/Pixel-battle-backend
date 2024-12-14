from datetime import UTC, datetime
from uuid import UUID

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, red
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.chunk_view import CollectionChunkView


excepted_pixel = Pixel(position=Vector(), color=red)


async def test_result(
    recolor_pixel: RecolorPixel[CollectionChunkView],
    stored_pixel: Pixel[RGBColor]  # noqa: ARG001
) -> None:
    datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
    output = await recolor_pixel(
        user_id=UUID(int=1),
        datetime_of_user_obtaining_recoloring_right=datetime_,
        pixel_position_x=0,
        pixel_position_y=0,
        chunk_number_x=0,
        chunk_number_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    assert output.pixel == excepted_pixel
    assert output.user.chunk == excepted_pixel.chunk


async def test_chunk_views(
    recolor_pixel: RecolorPixel[CollectionChunkView],
    stored_pixel: Pixel[RGBColor]  # noqa: ARG001
) -> None:
    datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
    await recolor_pixel(
        user_id=UUID(int=1),
        datetime_of_user_obtaining_recoloring_right=datetime_,
        pixel_position_x=0,
        pixel_position_y=0,
        chunk_number_x=0,
        chunk_number_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    raw_chunk_views = {
        chunk: set(view)
        for chunk, view in recolor_pixel.chunk_views.to_dict().items()
    }
    excepted_result = {excepted_pixel.chunk: {excepted_pixel}}

    assert raw_chunk_views == excepted_result
