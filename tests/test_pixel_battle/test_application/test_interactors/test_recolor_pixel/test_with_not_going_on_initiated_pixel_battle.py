from contextlib import suppress
from datetime import UTC, datetime

from pytest import fixture, raises

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.pixel import (
    PixelBattleIsNotGoingOnToRecolorError,
)
from pixel_battle.entities.core.pixel_battle import InitiatedPixelBattle
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@fixture
def input_signed_user_data() -> User:
    time = Time(datetime=datetime(2010, 1, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)


@fixture(autouse=True)
async def effect(recolor_pixel: RecolorPixel[User | None]) -> None:
    start_time = Time(datetime=datetime(1981, 1, 1, tzinfo=UTC))
    end_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))
    time_delta = TimeDelta(start_time=start_time, end_time=end_time)

    admin_key = AdminKey(token="token")
    pixel_battle = InitiatedPixelBattle(
        admin_key=admin_key, time_delta=time_delta
    )

    await recolor_pixel.pixel_battle_container.put(pixel_battle)


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
