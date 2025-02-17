from pytest import mark

from pixel_battle.presentation.distributed_tasks.refresh_chunk import (
    RefreshChunkCommand,
)


@mark.parametrize(
    "command",
    [
        RefreshChunkCommand(chunk_number_x=0, chunk_number_y=0),
        RefreshChunkCommand(chunk_number_x=9, chunk_number_y=9),
        RefreshChunkCommand(chunk_number_x=0, chunk_number_y=9),
        RefreshChunkCommand(chunk_number_x=9, chunk_number_y=0),
        RefreshChunkCommand(chunk_number_x=1, chunk_number_y=9),
        RefreshChunkCommand(chunk_number_x=9, chunk_number_y=1),
        RefreshChunkCommand(chunk_number_x=5, chunk_number_y=5),
    ],
)
def test_isomorphism(command: RefreshChunkCommand) -> None:
    next_command = RefreshChunkCommand.from_bytes(command.to_bytes())

    assert next_command == command
