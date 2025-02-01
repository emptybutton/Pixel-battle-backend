from datetime import UTC, datetime

from pytest import fixture, mark

from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@fixture
def time_delta() -> TimeDelta:
    start_time = Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))
    end_time = Time(datetime=datetime(2007, 1, 1, tzinfo=UTC))

    return TimeDelta(start_time=start_time, end_time=end_time)


@mark.parametrize(
    "time",
    [
        Time(datetime=datetime(2006, 1, 1, tzinfo=UTC)),
        Time(datetime=datetime(2006, 6, 1, tzinfo=UTC)),
        Time(datetime=datetime(2006, 12, 31, 23, 59, 59, 999, tzinfo=UTC)),
    ]
)
def test_contains(time_delta: TimeDelta, time: Time) -> None:
    assert time in time_delta


@mark.parametrize(
    "time",
    [
        Time(datetime=datetime(2005, 12, 31, 23, 59, 59, 999, tzinfo=UTC)),
        Time(datetime=datetime(2007, 1, 1, tzinfo=UTC)),
        Time(datetime=datetime(2010, 1, 1, tzinfo=UTC)),
        Time(datetime=datetime(2000, 1, 1, tzinfo=UTC)),
    ]
)
def test_not_contains(time_delta: TimeDelta, time: Time) -> None:
    assert time not in time_delta
