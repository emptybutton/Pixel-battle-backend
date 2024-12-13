from datetime import UTC, datetime
from uuid import UUID

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, white
from pixel_battle.entities.quantities.position import zero_position
from pixel_battle.infrastructure.adapters.pixels import InMemoryPixels


async def test_result(
    recolor_pixel: RecolorPixel[InMemoryPixels],
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
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    excepted_pixel = Pixel(position=zero_position, color=white)

    assert output.pixel == excepted_pixel
    assert output.user.chunk == recolor_pixel.chunk


async def test_stored_pixels(
    recolor_pixel: RecolorPixel[InMemoryPixels],
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
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert not recolor_pixel.pixels
