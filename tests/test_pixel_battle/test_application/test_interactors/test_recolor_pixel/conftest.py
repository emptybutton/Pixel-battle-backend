from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.pixel_battle import ScheduledPixelBattle
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.pixel_battle_container import (
    InMemoryPixelBattleContainer,
)
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)


@fixture
def recolor_pixel() -> RecolorPixel[User | None]:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    start_time = Time(datetime=datetime(1981, 1, 1, tzinfo=UTC))
    end_time = Time(datetime=datetime(2077, 1, 1, tzinfo=UTC))
    time_delta = TimeDelta(start_time=start_time, end_time=end_time)

    admin_key = AdminKey(token="token")
    pixel_battle = ScheduledPixelBattle(
        admin_key=admin_key, time_delta=time_delta
    )

    return RecolorPixel(
        user_data_signing=UserDataSigningAsIdentification(),
        pixel_queue=InMemoryPixelQueue(pulling_timeout_seconds=0),
        pixel_battle_container=InMemoryPixelBattleContainer(pixel_battle),
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
