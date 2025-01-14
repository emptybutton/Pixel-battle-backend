from pytest import mark

from pixel_battle.presentation.distributed_tasks.refresh_chunk_view import (
    RefreshChunkViewCommand,
)


@mark.parametrize(
    "command",
    [
        RefreshChunkViewCommand(chunk_number_x=0, chunk_number_y=0),
        RefreshChunkViewCommand(chunk_number_x=9, chunk_number_y=9),
        RefreshChunkViewCommand(chunk_number_x=0, chunk_number_y=9),
        RefreshChunkViewCommand(chunk_number_x=9, chunk_number_y=0),
        RefreshChunkViewCommand(chunk_number_x=1, chunk_number_y=9),
        RefreshChunkViewCommand(chunk_number_x=9, chunk_number_y=1),
        RefreshChunkViewCommand(chunk_number_x=5, chunk_number_y=5),
    ],
)
def test_isomorphism(command: RefreshChunkViewCommand) -> None:
    next_command = RefreshChunkViewCommand.from_bytes(command.to_bytes())

    assert next_command == command
