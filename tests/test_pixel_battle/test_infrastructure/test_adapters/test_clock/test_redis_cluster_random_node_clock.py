from datetime import UTC, datetime

from dirty_equals import IsDatetime
from pytest import fixture
from redis.asyncio import RedisCluster

from pixel_battle.infrastructure.adapters.clock import (
    RedisClusterRandomNodeClock,
)


@fixture
def clock(redis_cluster: RedisCluster) -> RedisClusterRandomNodeClock:
    return RedisClusterRandomNodeClock(redis_cluster=redis_cluster)


async def test_get_current_time(clock: RedisClusterRandomNodeClock) -> None:
    result_current_datetime = (await clock.get_current_time()).datetime
    local_current_datetime = datetime.now(UTC)

    assert result_current_datetime == IsDatetime(approx=local_current_datetime)
