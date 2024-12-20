from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.entities.core.user import (
    User,
    has_recoloring_right,
    time_of_obtaining_recoloring_right_when,
    user_temporarily_without_recoloring_right_when,
)
from pixel_battle.entities.quantities.time import Time


@fixture
def user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)


def test_time_of_obtaining_recoloring_right_when() -> None:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    result = time_of_obtaining_recoloring_right_when(current_time=current_time)

    excepted_result = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    assert result == excepted_result


def test_has_recoloring_right_is_true(user: User) -> None:
    current_time = user.time_of_obtaining_recoloring_right

    assert has_recoloring_right(user, current_time=current_time)


def test_has_recoloring_right_is_false(user: User) -> None:
    current_time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))

    assert not has_recoloring_right(user, current_time=current_time)


def test_temporarily_without_right_to_recolor(user: User) -> None:
    current_time = Time(datetime=datetime(2007, 1, 1, tzinfo=UTC))
    excepted_time = Time(datetime=datetime(2007, 1, 1, 0, 1, tzinfo=UTC))
    excepted_user = User(time_of_obtaining_recoloring_right=excepted_time)

    user = user_temporarily_without_recoloring_right_when(
        current_time=current_time
    )

    assert user == excepted_user
