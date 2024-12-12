from datetime import UTC, datetime
from uuid import uuid4

from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.user import (
    User,
    has_right_to_recolor,
    new_user_when,
    temporarily_without_right_to_recolor,
    time_of_obtaining_recoloring_right_when,
)
from pixel_battle.entities.quantities.time import Time


@fixture
def user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return User(
        id=uuid4(),
        time_of_obtaining_recoloring_right=time,
        chunk=Chunk(number=ChunkNumber(x=0, y=0)),
    )


def test_time_of_obtaining_recoloring_right_when() -> None:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    result = time_of_obtaining_recoloring_right_when(current_time=current_time)

    excepted_result = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    assert result == excepted_result


def test_has_right_to_recolor_is_true(user: User) -> None:
    current_time = user.time_of_obtaining_recoloring_right

    assert has_right_to_recolor(user, current_time=current_time)


def test_has_right_to_recolor_is_false(user: User) -> None:
    current_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))

    assert not has_right_to_recolor(user, current_time=current_time)


def test_temporarily_without_right_to_recolor(user: User) -> None:
    current_time = Time(datetime=datetime(2007, 1, 1, tzinfo=UTC))
    excepted_time = Time(datetime=datetime(2007, 1, 1, 0, 1, tzinfo=UTC))
    excepted_result = User(
        id=user.id,
        time_of_obtaining_recoloring_right=excepted_time,
        chunk=Chunk(number=ChunkNumber(x=0, y=0)),
    )

    result = temporarily_without_right_to_recolor(
        user, current_time=current_time
    )

    assert result == excepted_result


def test_new_user_when() -> None:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))
    excepted_time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    chunk = Chunk(number=ChunkNumber(x=0, y=0))

    new_user = new_user_when(current_time=current_time, chunk=chunk)

    assert new_user.chunk == chunk
    assert new_user.time_of_obtaining_recoloring_right == excepted_time
