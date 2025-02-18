from datetime import datetime

from click import IntRange, command, echo, option, style
from dishka import FromDishka

from pixel_battle.application.interactors.refresh_chunk import (
    RefreshChunk,
)
from pixel_battle.application.ports.chunk_view import ChunkView


@command()
@option(
    "-x",
    "--chunk-number-x",
    type=IntRange(0, 9),
    prompt="chunk.number.x",
    help="X coordinate of chunk number.",
)
@option(
    "-y",
    "--chunk-number-y",
    type=IntRange(0, 9),
    prompt="chunk.number.y",
    help="Y coordinate of chunk number.",
)
@option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Don't write to stdout.",
)
async def refresh_chunk_command(
    refresh_chunk: FromDishka[RefreshChunk[ChunkView]],
    chunk_number_x: int,
    chunk_number_y: int,
    quiet: bool,
) -> None:
    start_time = datetime.now()

    await refresh_chunk(chunk_number_x, chunk_number_y)

    end_time = datetime.now()
    time_delta = end_time - start_time
    delta_seconds = time_delta.total_seconds()

    if not quiet:
        styled_delta_seconds = style(delta_seconds, fg="cyan")
        echo(
            f"The chunk image was refreshed in {styled_delta_seconds} seconds."
        )
