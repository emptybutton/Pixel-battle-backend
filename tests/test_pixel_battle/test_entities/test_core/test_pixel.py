from datetime import UTC, datetime

from pytest import fixture, raises

from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import (
    Pixel,
    PixelBattleIsNotGoingOnToRecolorError,
    PixelOutOfCanvasError,
    RecoloredPixelByUser,
    UserHasNoRightToRecolorError,
    pixel_in,
    recolored,
    recolored_by_user,
)
from pixel_battle.entities.core.pixel_battle import (
    ScheduledPixelBattle,
    UnscheduledPixelBattle,
)
from pixel_battle.entities.core.user import User
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    RGBColor,
    black,
    white,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


def test_negative_pixel_position() -> None:
    with raises(PixelOutOfCanvasError):
        Pixel(position=Vector(x=-1, y=0), color=black)


def test_too_large_pixel_position() -> None:
    with raises(PixelOutOfCanvasError):
        Pixel(position=Vector(x=1601, y=400), color=black)


@fixture
def user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)


@fixture
def original_pixel() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=white)


@fixture
def recolored_pixel() -> Pixel[RGBColor]:
    return Pixel(position=Vector(), color=black)


@fixture
def admin_key() -> AdminKey:
    return AdminKey(token="token")


@fixture
def scheduled_pixel_battle(admin_key: AdminKey) -> ScheduledPixelBattle:
    start_time = Time(datetime=datetime(1981, 1, 1, tzinfo=UTC))
    end_time = Time(datetime=datetime(2020, 1, 1, tzinfo=UTC))
    time_delta = TimeDelta(start_time=start_time, end_time=end_time)

    return ScheduledPixelBattle(time_delta=time_delta, admin_key=admin_key)


@fixture
def unscheduled_pixel_battle(admin_key: AdminKey) -> UnscheduledPixelBattle:
    return UnscheduledPixelBattle(admin_key=admin_key)


def test_recolored(
    original_pixel: Pixel[RGBColor], recolored_pixel: Pixel[RGBColor]
) -> None:
    new_color = recolored_pixel.color

    assert recolored(original_pixel, new_color=new_color) == recolored_pixel


def test_recolored_by_user(
    user: User,
    original_pixel: Pixel[RGBColor],
    recolored_pixel: Pixel[RGBColor],
    scheduled_pixel_battle: ScheduledPixelBattle,
) -> None:
    new_color = recolored_pixel.color
    current_time = user.time_of_obtaining_recoloring_right

    result = recolored_by_user(
        original_pixel,
        user=user,
        new_color=new_color,
        current_time=current_time,
        pixel_battle=scheduled_pixel_battle,
    )

    excepted_user_time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    excepted_user = User(time_of_obtaining_recoloring_right=excepted_user_time)
    excepted_result = RecoloredPixelByUser(
        user=excepted_user, pixel=recolored_pixel
    )

    assert result == excepted_result


def test_recolored_by_user_without_right(
    user: User,
    original_pixel: Pixel[RGBColor],
    recolored_pixel: Pixel[RGBColor],
    scheduled_pixel_battle: ScheduledPixelBattle,
) -> None:
    new_color = recolored_pixel.color
    current_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))

    with raises(UserHasNoRightToRecolorError):
        recolored_by_user(
            original_pixel,
            user=user,
            new_color=new_color,
            current_time=current_time,
            pixel_battle=scheduled_pixel_battle,
        )


def test_recolored_by_with_unscheduled_pixel_battle(
    user: User,
    original_pixel: Pixel[RGBColor],
    recolored_pixel: Pixel[RGBColor],
    unscheduled_pixel_battle: UnscheduledPixelBattle,
) -> None:
    with raises(PixelBattleIsNotGoingOnToRecolorError):
        recolored_by_user(
            original_pixel,
            user=user,
            new_color=recolored_pixel.color,
            current_time=user.time_of_obtaining_recoloring_right,
            pixel_battle=unscheduled_pixel_battle,
        )


def test_recolored_by_with_not_going_on_pixel_battle(
    user: User,
    original_pixel: Pixel[RGBColor],
    recolored_pixel: Pixel[RGBColor],
    scheduled_pixel_battle: ScheduledPixelBattle,
) -> None:
    current_time = Time(datetime=datetime(2077, 1, 1, tzinfo=UTC))

    with raises(PixelBattleIsNotGoingOnToRecolorError):
        recolored_by_user(
            original_pixel,
            user=user,
            new_color=recolored_pixel.color,
            current_time=current_time,
            pixel_battle=scheduled_pixel_battle,
        )


def test_pixel_in() -> None:
    chunk = Chunk(number=ChunkNumber(x=1, y=2))
    position_within_chunk = Vector(x=51, y=99)

    pixel = pixel_in(
        chunk, color=white, position_within_chunk=position_within_chunk
    )

    assert pixel == Pixel(color=white, position=Vector(x=151, y=299))
