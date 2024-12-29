from datetime import UTC, datetime

from pytest import fixture, raises

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import (
    Pixel,
    PixelOutOfCanvasError,
    RecoloredPixelByUser,
    UserHasNoRightToRecolorError,
    pixel_in,
    recolored,
    recolored_by_user,
)
from pixel_battle.entities.core.user import User
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    black,
    white,
)
from pixel_battle.entities.space.time import Time


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
def original_pixel() -> User:
    return Pixel(position=Vector(), color=white)


@fixture
def recolored_pixel() -> User:
    return Pixel(position=Vector(), color=black)


def test_recolored(original_pixel: Pixel, recolored_pixel: Pixel) -> None:
    new_color = recolored_pixel.color

    assert recolored(original_pixel, new_color=new_color) == recolored_pixel


def test_recolored_by_user(
    user: User, original_pixel: Pixel, recolored_pixel: Pixel
) -> None:
    new_color = recolored_pixel.color
    current_time = user.time_of_obtaining_recoloring_right

    result = recolored_by_user(
        original_pixel,
        user=user,
        new_color=new_color,
        current_time=current_time,
    )

    excepted_user_time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    excepted_user = User(time_of_obtaining_recoloring_right=excepted_user_time)
    excepted_result = RecoloredPixelByUser(
        user=excepted_user, pixel=recolored_pixel
    )

    assert result == excepted_result


def test_recolored_by_user_without_right(
    user: User, original_pixel: Pixel, recolored_pixel: Pixel
) -> None:
    new_color = recolored_pixel.color
    current_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))

    with raises(UserHasNoRightToRecolorError):
        recolored_by_user(
            original_pixel,
            user=user,
            new_color=new_color,
            current_time=current_time,
        )


def test_pixel_in() -> None:
    chunk = Chunk(number=ChunkNumber(x=1, y=2))
    position_within_chunk = Vector(x=51, y=99)

    pixel = pixel_in(
        chunk, color=white, position_within_chunk=position_within_chunk
    )

    assert pixel == Pixel(color=white, position=Vector(x=151, y=299))
