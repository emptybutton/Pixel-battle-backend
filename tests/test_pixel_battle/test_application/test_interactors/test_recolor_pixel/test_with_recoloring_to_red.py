from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, red
from pixel_battle.entities.quantities.vector import Vector


@fixture
def expected_pixel() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=red)


async def test_result(
    recolor_pixel: RecolorPixel, expected_pixel: Pixel[RGBColor]
) -> None:
    datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
    output = await recolor_pixel(
        datetime_of_obtaining_recoloring_right=datetime_,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    assert output.pixel == expected_pixel


async def test_broker(
    recolor_pixel: RecolorPixel, expected_pixel: Pixel[RGBColor]
) -> None:
    datetime_ = datetime(2006, 1, 1, tzinfo=UTC)
    await recolor_pixel(
        datetime_of_obtaining_recoloring_right=datetime_,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    expected_result = {expected_pixel.chunk: [expected_pixel]}

    assert dict(recolor_pixel.broker) == expected_result
