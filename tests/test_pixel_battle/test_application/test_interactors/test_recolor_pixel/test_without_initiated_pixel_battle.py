from contextlib import suppress
from datetime import UTC, datetime

from pytest import fixture, raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import (
    PixelBattleIsNotGoingOnToRecolorError,
)
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time


@fixture
def input_signed_user_data() -> User:
    time = Time(datetime=datetime(2010, 1, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)


@fixture(autouse=True)
async def effect(recolor_pixel: RecolorPixel[User | None]) -> None:
    await recolor_pixel.pixel_battle_container.put(None)


async def test_result(
    recolor_pixel: RecolorPixel[User | None],
    input_signed_user_data: User,
) -> None:
    with raises(PixelBattleIsNotGoingOnToRecolorError):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )


async def test_pixel_queue(
    recolor_pixel: RecolorPixel[User | None],
    input_signed_user_data: User,
) -> None:
    with suppress(Exception):
        await recolor_pixel(
            signed_user_data=input_signed_user_data,
            pixel_position_x=0,
            pixel_position_y=0,
            new_color_red_value_number=255,
            new_color_green_value_number=255,
            new_color_blue_value_number=255,
        )

    assert not recolor_pixel.pixel_queue
