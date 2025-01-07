from datetime import UTC, datetime

from dirty_equals import IsDatetime
from pytest import fixture

from pixel_battle.infrastructure.adapters.clock import LocalClock


@fixture
def clock() -> LocalClock:
    return LocalClock()


async def test_get_current_time(clock: LocalClock) -> None:
    excepted_current_datetime = datetime.now(UTC)
    result_current_time = await clock.get_current_time()

    operand = IsDatetime(approx=excepted_current_datetime)
    assert result_current_time.datetime == operand
