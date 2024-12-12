from datetime import UTC, datetime, timedelta

from pytest import fixture, raises

from pixel_battle.entities.quantities.time import NotUTCTimeError, Time


def test_creation_with_not_utc_datetime() -> None:
    with raises(NotUTCTimeError):
        Time(datetime=datetime(2006, 1, 1))


def test_ok_creation() -> None:
    Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))


@fixture
def time1() -> Time:
    return Time(datetime=datetime(2006, 1, 1, tzinfo=UTC))


@fixture
def time2() -> Time:
    return Time(datetime=datetime(2006, 1, 2, tzinfo=UTC))


def test_map(time1: Time, time2: Time) -> None:
    result = time1.map(lambda datetime: datetime + timedelta(days=1))

    assert result == time2


def test_gt(time1: Time, time2: Time) -> None:
    assert time2 > time1


def test_ge_with_different_times(time1: Time, time2: Time) -> None:
    assert time2 >= time1


def test_ge_with_same_time(time1: Time) -> None:
    assert time1 >= time1


def test_lt(time1: Time, time2: Time) -> None:
    assert time1 < time2


def test_le_with_different_times(time1: Time, time2: Time) -> None:
    assert time1 <= time2


def test_le_with_same_time(time1: Time) -> None:
    assert time1 <= time1
