from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time


@fixture
def user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)
