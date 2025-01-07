import sys
from dataclasses import dataclass
from datetime import datetime
from io import TextIOBase
from typing import Any, cast

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateChunkViewScript:
    update_chunk_view: UpdateChunkView[ChunkView, Any]
    ok_file: TextIOBase = cast(TextIOBase, sys.stdout)
    error_file: TextIOBase = cast(TextIOBase, sys.stderr)

    async def __call__(self) -> None:
        if self.__is_help():
            self.__print_help()

        args = self.__parse_args()

        if args is None:
            return

        chunk_number_x, chunk_number_y = args

        self.__print("Updating...")
        start_time = datetime.now()

        await self.update_chunk_view(chunk_number_x, chunk_number_y)

        end_time = datetime.now()
        time_delta = end_time - start_time

        self.__print(f"The chunk view was updated. (Finished in {time_delta})")

    def __is_help(self) -> bool:
        has_flag = len(sys.argv) == 2 and sys.argv[1] == "--help"  # noqa: PLR2004
        has_args = len(sys.argv) > 1

        return has_flag or not has_args

    def __parse_args(self) -> tuple[int, int] | None:
        if len(sys.argv) != 3:  # noqa: PLR2004
            self.__print_error()
            return None

        try:
            chunk_number_x, chunk_number_y = int(sys.argv[1]), int(sys.argv[2])
        except ValueError:
            self.__print_error()
            return None

        if chunk_number_x not in range(10) or chunk_number_y not in range(10):
            self.__print_error()
            return None

        return chunk_number_x, chunk_number_y

    def __print_error(self) -> None:
        text = "Coordinates must be numbers in range(0, 10)."
        self.__print(text, panic=True)

    def __print_help(self) -> None:
        text = (
            "\nUsage:  python [script_path] [chunk_number_x] [chunk_number_y]"
            "\n\nCoordinates must be numbers in range(0, 10)."
        )
        self.__print(text)

    def __print(self, text: str, *, panic: bool = False) -> None:
        print(text, file=self.error_file if panic else self.ok_file)
