from dataclasses import dataclass
from datetime import UTC, datetime

from redis.asyncio import RedisCluster

from pixel_battle.application.ports.clock import Clock
from pixel_battle.entities.space.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class StoppedClock(Clock):
    current_time: Time

    async def get_current_time(self) -> Time:
        return self.current_time


@dataclass(kw_only=True, frozen=True, slots=True)
class LocalClock(Clock):
    async def get_current_time(self) -> Time:
        local_datetime = datetime.now(UTC)

        return Time(datetime=local_datetime)


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisClusterRandomNodeClock(Clock):
    redis_cluster: RedisCluster

    async def get_current_time(self) -> Time:
        rounded_timestamp, microseconds = await self.redis_cluster.time(
            target_nodes=RedisCluster.RANDOM
        )

        timestamp = rounded_timestamp + microseconds / 1_000_000
        datetime_ = datetime.fromtimestamp(timestamp, tz=UTC)

        return Time(datetime=datetime_)
