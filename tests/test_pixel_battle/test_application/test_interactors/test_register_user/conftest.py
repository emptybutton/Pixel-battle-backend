from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.application.interactors.register_user import (
    RegisterUser,
)
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)


@fixture
def register_user(current_time: Time) -> RegisterUser:
    return RegisterUser(
        user_data_signing=UserDataSigningAsIdentification(),
        clock=StoppedClock(current_time=current_time),
    )


@fixture
def current_time() -> Time:
    return Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))


@fixture
def registered_user() -> User:
    time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))
    return User(time_of_obtaining_recoloring_right=time)
