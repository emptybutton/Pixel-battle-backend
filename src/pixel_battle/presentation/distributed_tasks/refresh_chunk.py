from asyncio import sleep
from dataclasses import dataclass
from typing import Any, ClassVar, NoReturn, cast

from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.refresh_chunk import (
    RefreshChunk,
)
from pixel_battle.infrastructure.encoding import (
    decoded_chunk_data_when,
    encoded_chunk_from_data_when,
)


class RefreshChunkCommandError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshChunkCommand:
    chunk_number_x: int
    chunk_number_y: int

    def __post_init__(self) -> None:
        is_chunk_number_x_valid = self.chunk_number_x in range(10)
        is_chunk_number_y_valid = self.chunk_number_y in range(10)

        if not is_chunk_number_x_valid or not is_chunk_number_y_valid:
            raise RefreshChunkCommandError(str(self))

    def to_bytes(self) -> bytes:
        chunk_data = (self.chunk_number_x, self.chunk_number_y)
        return encoded_chunk_from_data_when(chunk_data=chunk_data)

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "RefreshChunkCommand":
        x, y = decoded_chunk_data_when(encoded_chunk=bytes_)

        return RefreshChunkCommand(chunk_number_x=x, chunk_number_y=y)


@dataclass(kw_only=True, frozen=True)
class RefreshChunkTask:
    refresh_chunk: RefreshChunk[Any]
    redis_cluster: RedisCluster
    pulling_interval_seconds: int
    __queue_key: ClassVar = b"task_{{0}}_queue"
    __queue_lock_key: ClassVar = b"task_{{0}}_queue_lock"
    __command_count: ClassVar = 100

    async def start_pushing(self) -> NoReturn:
        while True:
            await self.__push_commands()
            await sleep(self.pulling_interval_seconds)

    async def start_pulling(self) -> NoReturn:
        while True:
            command = await self.__pull_one_command()
            await self.__execute(command)

    async def __pull_one_command(self) -> RefreshChunkCommand:
        _, encoded_command = await self.redis_cluster.blpop([self.__queue_key])  # type: ignore[misc]
        print(f"PULL: {encoded_command}", flush=True)

        return RefreshChunkCommand.from_bytes(encoded_command)

    async def __push_commands(self) -> None:
        pipe = self.redis_cluster.pipeline()
        pipe.llen(self.__queue_key)
        pipe.lindex(self.__queue_key, -1)
        pipe.set(self.__queue_lock_key, 1, nx=True, ex=20)

        result = cast(
            tuple[int, bytes | None, bytes | None, bool | None],
            await pipe.execute(),
        )
        stored_command_count = result[0]
        last_stored_encoded_command = result[1]
        is_queue_lock_acquired = result[2]

        if is_queue_lock_acquired is None:
            return

        unstored_encoded_commands = self.__unstored_encoded_commands_when(
            stored_command_count=stored_command_count,
            last_stored_encoded_command=last_stored_encoded_command,
        )

        pipe = self.redis_cluster.pipeline()

        if unstored_encoded_commands:
            repr_commands = list(unstored_encoded_commands)
            print(f"PUSH {len(repr_commands)}: {repr_commands}", flush=True)

            pipe.rpush(self.__queue_key, *unstored_encoded_commands)

        pipe.delete(self.__queue_lock_key)
        await pipe.execute()

    def __unstored_encoded_commands_when(
        self,
        *,
        stored_command_count: int,
        last_stored_encoded_command: bytes | None,
    ) -> tuple[bytes, ...]:
        unstored_command_count = self.__unstored_command_count_when(
            stored_command_count=stored_command_count
        )

        if last_stored_encoded_command is not None:
            return self.__next_encoded_commands_when(
                encoded_command=last_stored_encoded_command,
                next_command_count=unstored_command_count,
            )

        first_encoded_command = bytes([0])
        other_encoded_commands = self.__next_encoded_commands_when(
            encoded_command=first_encoded_command,
            next_command_count=unstored_command_count - 1,
        )

        return (first_encoded_command, *other_encoded_commands)

    def __next_encoded_commands_when(
        self, encoded_command: bytes, next_command_count: int
    ) -> tuple[bytes, ...]:
        return tuple(
            self.__next_encoded_command_when(
                encoded_command=encoded_command,
                offset=offset,
            )
            for offset in range(1, next_command_count + 1)
        )

    def __next_encoded_command_when(
        self, *, encoded_command: bytes, offset: int
    ) -> bytes:
        encoded_command_byte = ord(encoded_command) + offset

        if encoded_command_byte > self.__command_count - 1:
            encoded_command_byte -= (
                (encoded_command_byte // self.__command_count)
                * self.__command_count
            )

        return bytes([encoded_command_byte])

    def __unstored_command_count_when(
        self, *, stored_command_count: int
    ) -> int:
        if stored_command_count > self.__command_count:
            return 0

        return self.__command_count - stored_command_count  # type: ignore[no-any-return]

    async def __execute(self, command: RefreshChunkCommand) -> None:
        await self.refresh_chunk(
            command.chunk_number_x, command.chunk_number_y
        )
