from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.core.user import User
from pixel_battle.entities.quantities.color import RGBColor, red
from pixel_battle.entities.quantities.vector import Vector


@fixture
def expected_pixel() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=red)


async def test_result(
    recolor_pixel: RecolorPixel,
    expected_pixel: Pixel[RGBColor],
    signed_user_data: User,
) -> None:
    output = await recolor_pixel(
        signed_user_data=signed_user_data,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    assert output.pixel == expected_pixel


async def test_broker(
    recolor_pixel: RecolorPixel,
    expected_pixel: Pixel[RGBColor],
    signed_user_data: User,
) -> None:
    await recolor_pixel(
        signed_user_data=signed_user_data,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    expected_result = {expected_pixel.chunk: [expected_pixel]}

    assert dict(recolor_pixel.broker) == expected_result
