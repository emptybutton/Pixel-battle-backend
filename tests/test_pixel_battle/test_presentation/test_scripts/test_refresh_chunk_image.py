from io import StringIO
from sys import argv

from pytest import fixture, mark

from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultCollectionChunkViewWhen,
)
from pixel_battle.infrastructure.adapters.chunk_views import InMemoryChunkViews
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue
from pixel_battle.presentation.scripts.refresh_chunk_image import (
    RefreshChunkImageScript,
)


type Script = RefreshChunkImageScript


@fixture
def script() -> Script:
    ok_file = StringIO()
    error_file = StringIO()

    refresh_chunk_view = RefreshChunkView(
        pixel_queue=InMemoryPixelQueue(),
        default_chunk_view_when=DefaultCollectionChunkViewWhen(),
        chunk_views=InMemoryChunkViews(),
    )

    return RefreshChunkImageScript(
        ok_file=ok_file,
        error_file=error_file,
        refresh_chunk_view=refresh_chunk_view,
    )


async def test_ok(script: Script) -> None:
    argv[:] = ["_", "0", "0"]

    await script()

    output = script.ok_file.getvalue().split("\n")

    assert output[0].startswith("The chunk image was refreshed. (Lasted ")
    assert output[0].endswith(" seconds)")


@mark.parametrize(
    "args", (["0", "99"], ["-1", "0"], ["X", "0"], ["9"], ["--helps"])
)
async def test_with_invalid_args(script: Script, args: list[str]) -> None:
    argv[:] = ["_", *args]

    await script()

    output = script.error_file.getvalue()
    assert output == "Coordinates must be numbers in range(0, 10).\n"


async def test_help_by_flag(script: Script) -> None:
    argv[:] = ["_", "--help"]

    await script()

    output = script.ok_file.getvalue()
    excepted_output = (
        "\nUsage:  python [script_path] [chunk_number_x] [chunk_number_y]"
        "\n\nCoordinates must be numbers in range(0, 10).\n"
    )

    assert output == excepted_output


async def test_help_by_args(script: Script) -> None:
    argv[:] = ["_"]

    await script()

    output = script.ok_file.getvalue()
    excepted_output = (
        "\nUsage:  python [script_path] [chunk_number_x] [chunk_number_y]"
        "\n\nCoordinates must be numbers in range(0, 10).\n"
    )

    assert output == excepted_output
