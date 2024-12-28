from datetime import UTC, datetime

from pytest import fixture

from pixel_battle.entities.quantities.time import Time
from pixel_battle.infrastructure.adapters.clock import StoppedClock


@fixture
def clock() -> StoppedClock:
    current_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))

    return StoppedClock(current_time=current_time)


async def test_get_current_time(clock: StoppedClock) -> None:
    result_current_time = await clock.get_current_time()

    assert result_current_time == clock.current_time
