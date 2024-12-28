from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.user import User
from pixel_battle.entities.quantities.time import Time
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)


@fixture
def recolor_pixel() -> RecolorPixel:
    return RecolorPixel(
        user_data_signing=UserDataSigningAsIdentification(),
        broker=InMemoryBroker(),
    )


@fixture
def signed_user_data() -> User:
    time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return User(time_of_obtaining_recoloring_right=time)
