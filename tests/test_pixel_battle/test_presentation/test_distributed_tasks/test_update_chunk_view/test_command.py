from pytest import mark

from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewCommand,
)


@mark.parametrize(
    "command",
    [
        UpdateChunkViewCommand(chunk_number_x=0, chunk_number_y=0),
        UpdateChunkViewCommand(chunk_number_x=9, chunk_number_y=9),
        UpdateChunkViewCommand(chunk_number_x=0, chunk_number_y=9),
        UpdateChunkViewCommand(chunk_number_x=9, chunk_number_y=0),
        UpdateChunkViewCommand(chunk_number_x=1, chunk_number_y=9),
        UpdateChunkViewCommand(chunk_number_x=9, chunk_number_y=1),
        UpdateChunkViewCommand(chunk_number_x=5, chunk_number_y=5),
    ],
)
def test_isomorphism(command: UpdateChunkViewCommand) -> None:
    next_command = UpdateChunkViewCommand.from_bytes(command.to_bytes())

    assert next_command == command
