from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Iterable, Iterator
from uuid import UUID

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.users import Users
from pixel_battle.entities.core.user import User
from pixel_battle.entities.quantities.time import Time


@dataclass(init=False)
class InMemoryUsers(Users):
    __user_by_id: dict[UUID, User]

    def __init__(self, users: Iterable[User]) -> None:
        self.__user_by_id = {user.id: user for user in users}

    def __iter__(self) -> Iterator[User]:
        return iter(self.__user_by_id.values())

    def __len__(self) -> int:
        return len(self.__user_by_id)

    def __bool__(self) -> bool:
        return bool(self.__user_by_id)

    async def user_with_id(self, id: UUID) -> User | None:
        return self.__user_by_id.get(id)

    async def put(self, user: User) -> None:
        self.__user_by_id[user.id] = user


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterUsers(Users):
    redis_cluster: RedisCluster

    async def user_with_id(self, user_id: UUID) -> User | None:
        value = await self.redis_cluster.get(self.__key_by(user_id))

        if value is None:
            return None

        datetime_ = datetime.fromtimestamp(value, tz=UTC)
        time = Time(datetime=datetime_)

        return User(id=user_id, time_of_obtaining_recoloring_right=time)

    async def put(self, user: User) -> None:
        key = self.__key_by(user.id)
        value = self.__value_of(user)

        await self.redis_cluster.set(key, value, ex=10 * 60)

    def __key_by(self, user_id: UUID) -> bytes:
        return user_id.bytes + b"user"

    def __value_of(self, user: User) -> float:
        return user.time_of_obtaining_recoloring_right.datetime.timestamp()
