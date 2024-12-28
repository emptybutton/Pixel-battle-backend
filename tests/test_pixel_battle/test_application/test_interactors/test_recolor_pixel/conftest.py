from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.user import User
from pixel_battle.entities.quantities.time import Time
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)


@fixture
def recolor_pixel() -> RecolorPixel:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return RecolorPixel(
        user_data_signing=UserDataSigningAsIdentification(),
        broker=InMemoryBroker(),
        clock=StoppedClock(current_time=current_time),
    )


@fixture
def input_signed_user_data() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return User(time_of_obtaining_recoloring_right=time)


@fixture
def output_signed_user_data() -> User:
    time = Time(datetime=datetime(2006, 1, 1, 0, 1, tzinfo=UTC))

    return User(time_of_obtaining_recoloring_right=time)
