from asyncio import get_event_loop, sleep
from dataclasses import dataclass
from itertools import product
from typing import (
    Any,
    ClassVar,
    Iterable,
    NoReturn,
)

from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView as Interactor,
)


class UpdateChunkViewCommandError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateChunkViewCommand:
    chunk_number_x: int
    chunk_number_y: int

    def __post_init__(self) -> None:
        is_chunk_number_x_valid = self.chunk_number_x in range(10)
        is_chunk_number_y_valid = self.chunk_number_y in range(10)

        if not is_chunk_number_x_valid or not is_chunk_number_y_valid:
            raise UpdateChunkViewCommandError(str(self))

    def to_bytes(self) -> bytes:
        return bytes([self.chunk_number_x * 10 + self.chunk_number_y])

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "UpdateChunkViewCommand":
        chunk_number_x = bytes_[0] // 10
        chunk_number_y = bytes_[0] - chunk_number_x

        return UpdateChunkViewCommand(
            chunk_number_x=chunk_number_x, chunk_number_y=chunk_number_y
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateChunkViewTask:
    redis_cluster: RedisCluster
    interactor: Interactor[Any, Any]
    __queue_key: ClassVar = b"update_chunk_view"
    __loop_tasks: ClassVar = set()

    async def push(self) -> NoReturn:
        while True:
            await self.__send_for_execution(self.__commands_to_push)
            await sleep(2)

    async def pull(self) -> NoReturn:
        loop = get_event_loop()

        while True:
            command = await self.__pull_one_command()

            task = loop.create_task(self.__execute(command))
            task.add_done_callback(self.__loop_tasks.discard)

    async def __send_for_execution(
        self, commands: Iterable[UpdateChunkViewCommand]
    ) -> None:
        command_list_data = (command.to_bytes() for command in commands)
        mapping = {data: 0 for data in command_list_data}

        await self.redis_cluster.zadd(self.__queue_key, mapping)

    async def __pull_one_command(self) -> UpdateChunkViewCommand:
        result = await self.redis_cluster.bzmpop(  # type: ignore[misc]
            0, 1, [self.__queue_key], min=True
        )
        command_bytes: bytes = result[1][0][0]

        return UpdateChunkViewCommand.from_bytes(command_bytes)

    async def __execute(self, command: UpdateChunkViewCommand) -> None:
        await self.interactor(command.chunk_number_x, command.chunk_number_y)

    @property
    def __commands_to_push(self) -> Iterable[UpdateChunkViewCommand]:
        for chunk_number_x, chunk_number_y in product(range(10), repeat=2):
            yield UpdateChunkViewCommand(
                chunk_number_x=chunk_number_x, chunk_number_y=chunk_number_y
            )
