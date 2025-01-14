from asyncio import sleep
from dataclasses import dataclass
from functools import cached_property
from itertools import product
from typing import Any, ClassVar, NoReturn

from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
)


class RefreshChunkViewCommandError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshChunkViewCommand:
    chunk_number_x: int
    chunk_number_y: int

    def __post_init__(self) -> None:
        is_chunk_number_x_valid = self.chunk_number_x in range(10)
        is_chunk_number_y_valid = self.chunk_number_y in range(10)

        if not is_chunk_number_x_valid or not is_chunk_number_y_valid:
            raise RefreshChunkViewCommandError(str(self))

    def to_bytes(self) -> bytes:
        return bytes([self.chunk_number_x * 10 + self.chunk_number_y])

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "RefreshChunkViewCommand":
        chunk_number_x = bytes_[0] // 10
        chunk_number_y = bytes_[0] - chunk_number_x * 10

        return RefreshChunkViewCommand(
            chunk_number_x=chunk_number_x, chunk_number_y=chunk_number_y
        )


@dataclass(kw_only=True, frozen=True)
class RefreshChunkViewTask:
    refresh_chunk_view: RefreshChunkView[Any]
    redis_cluster: RedisCluster
    __queue_key: ClassVar = b"refresh_chunk_view"

    async def start_pushing(self) -> NoReturn:
        while True:
            await sleep(2)
            await self.__push_commands()

    async def start_pulling(self) -> NoReturn:
        while True:
            command = await self.__pull_one_command()
            await self.__execute(command)

    async def __pull_one_command(self) -> RefreshChunkViewCommand:
        result = await self.redis_cluster.bzmpop(  # type: ignore[misc]
            0, 1, [self.__queue_key], min=True
        )
        command_bytes: bytes = result[1][0][0]

        return RefreshChunkViewCommand.from_bytes(command_bytes)

    async def __push_commands(self) -> None:
        await self.redis_cluster.zadd(self.__queue_key, self.__mapping_to_push)

    async def __execute(self, command: RefreshChunkViewCommand) -> None:
        await self.refresh_chunk_view(
            command.chunk_number_x, command.chunk_number_y
        )

    @cached_property
    def __mapping_to_push(self) -> dict[bytes, int]:
        commands = (
            RefreshChunkViewCommand(
                chunk_number_x=chunk_number_x, chunk_number_y=chunk_number_y
            )
            for chunk_number_x, chunk_number_y in product(range(10), repeat=2)
        )

        return {command.to_bytes(): 0 for command in commands}
