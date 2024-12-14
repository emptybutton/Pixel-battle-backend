from datetime import UTC, datetime
from uuid import uuid4

from pytest import fixture, raises

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import (
    Pixel,
    PixelOutOfCanvasError,
    PixelRecoloringByUser,
    UserHasNoRightToRecolorError,
    UserInDifferentChunkToRecolorError,
    recolored,
    recolored_by,
)
from pixel_battle.entities.core.user import User
from pixel_battle.entities.quantities.color import (
    black,
    white,
)
from pixel_battle.entities.quantities.time import Time
from pixel_battle.entities.quantities.vector import Vector


def test_negative_pixel_position() -> None:
    with raises(PixelOutOfCanvasError):
        Pixel(position=Vector(x=-1, y=0), color=black)


def test_too_large_pixel_position() -> None:
    with raises(PixelOutOfCanvasError):
        Pixel(position=Vector(x=1601, y=400), color=black)


@fixture
def user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return User(
        id=uuid4(),
        time_of_obtaining_recoloring_right=time,
        chunk=Chunk(number=ChunkNumber(x=0, y=0)),
    )


@fixture
def user_from_other_chunk() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return User(
        id=uuid4(),
        time_of_obtaining_recoloring_right=time,
        chunk=Chunk(number=ChunkNumber(x=1, y=1)),
    )


@fixture
def original_pixel() -> User:
    return Pixel(position=Vector(), color=white)


@fixture
def recolored_pixel() -> User:
    return Pixel(position=Vector(), color=black)


def test_recolored(original_pixel: Pixel, recolored_pixel: Pixel) -> None:
    new_color = recolored_pixel.color

    assert recolored(original_pixel, new_color=new_color) == recolored_pixel


def test_recolored_by(
    user: User, original_pixel: Pixel, recolored_pixel: Pixel
) -> None:
    new_color = recolored_pixel.color
    current_time = user.time_of_obtaining_recoloring_right

    result = recolored_by(
        user, original_pixel, new_color=new_color, current_time=current_time
    )

    excepted_user_time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    excepted_user = User(
        id=user.id,
        time_of_obtaining_recoloring_right=excepted_user_time,
        chunk=user.chunk,
    )
    excepted_result = PixelRecoloringByUser(
        user=excepted_user, pixel=recolored_pixel
    )

    assert result == excepted_result


def test_recolored_by_without_right(
    user: User, original_pixel: Pixel, recolored_pixel: Pixel
) -> None:
    new_color = recolored_pixel.color
    current_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))

    with raises(UserHasNoRightToRecolorError):
        recolored_by(
            user, original_pixel, new_color=new_color, current_time=current_time
        )


def test_recolored_from_other_chunk(
    user_from_other_chunk: User, original_pixel: Pixel, recolored_pixel: Pixel
) -> None:
    new_color = recolored_pixel.color
    current_time = user_from_other_chunk.time_of_obtaining_recoloring_right

    with raises(UserInDifferentChunkToRecolorError):
        recolored_by(
            user_from_other_chunk,
            original_pixel,
            new_color=new_color,
            current_time=current_time,
        )
