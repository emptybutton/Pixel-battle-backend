from typing import TYPE_CHECKING

from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import (
    Output,
    RecolorPixel,
)
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.core.user import User
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, red


if TYPE_CHECKING:
    from pixel_battle.entities.core.chunk import Chunk


@fixture
def expected_pixel() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=red)


async def test_result(
    recolor_pixel: RecolorPixel[User | None],
    expected_pixel: Pixel[RGBColor],
    input_signed_user_data: User,
    output_signed_user_data: User,
) -> None:
    result = await recolor_pixel(
        signed_user_data=input_signed_user_data,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    expected_result = Output(
        pixel=expected_pixel, signed_user_data=output_signed_user_data
    )

    assert result == expected_result


async def test_broker(
    recolor_pixel: RecolorPixel[User | None],
    expected_pixel: Pixel[RGBColor],
    input_signed_user_data: User,
) -> None:
    await recolor_pixel(
        signed_user_data=input_signed_user_data,
        pixel_position_x=0,
        pixel_position_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=0,
        new_color_blue_value_number=0,
    )

    expected_result = {expected_pixel.chunk: [expected_pixel]}
    result: dict[Chunk, list[Pixel[RGBColor]]] = dict(recolor_pixel.pixel_queue)  # type: ignore[call-overload]

    assert result == expected_result
