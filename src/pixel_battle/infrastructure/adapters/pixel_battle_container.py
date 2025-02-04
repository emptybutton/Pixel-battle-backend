from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar

from redis.asyncio import RedisCluster

from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.pixel_battle import (
    PixelBattle,
    ScheduledPixelBattle,
    UnscheduledPixelBattle,
    is_scheduled,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(slots=True)
class InMemoryPixelBattleContainer(PixelBattleContainer):
    _pixel_battle: PixelBattle

    async def put(self, pixel_battle: PixelBattle) -> None:
        self._pixel_battle = pixel_battle

    async def get(self) -> PixelBattle:
        return self._pixel_battle


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisClusterPixelBattleContainer(PixelBattleContainer):
    redis_cluster: RedisCluster
    admin_key: AdminKey

    __key: ClassVar = b"pixel_battle"
    __EncodedData: ClassVar = dict[str, Any]

    async def put(self, pixel_battle: PixelBattle) -> None:
        data = self.__encoded(pixel_battle)
        await self.redis_cluster.hset(self.__key, mapping=data)  # type: ignore[misc]

    async def get(self) -> PixelBattle:
        data = await self.redis_cluster.hgetall(self.__key)  # type: ignore[misc]
        return self.__decoded(data)

    def __encoded(self, pixel_battle: PixelBattle) -> __EncodedData:
        if not is_scheduled(pixel_battle):
            return {}

        time_delta = pixel_battle.time_delta

        return {
            b"start_datetime": time_delta.start_time.datetime.isoformat(),
            b"end_datetime": time_delta.end_time.datetime.isoformat(),
        }

    def __decoded(self, data: __EncodedData) -> PixelBattle:
        if not data:
            return UnscheduledPixelBattle(admin_key=self.admin_key)

        start_datetime = datetime.fromisoformat(
            data[b"start_datetime"].decode()
        )
        end_datetime = datetime.fromisoformat(data[b"end_datetime"].decode())

        start_time = Time(datetime=start_datetime)
        end_time = Time(datetime=end_datetime)
        time_delta = TimeDelta(start_time=start_time, end_time=end_time)

        return ScheduledPixelBattle(
            admin_key=self.admin_key, time_delta=time_delta
        )
