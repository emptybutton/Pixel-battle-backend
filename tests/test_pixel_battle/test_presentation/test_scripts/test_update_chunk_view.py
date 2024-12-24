from io import StringIO
from sys import argv

from pytest import fixture, mark

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView as Interactor,
)
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultCollectionChunkViewWhere,
)
from pixel_battle.infrastructure.adapters.chunk_views import InMemoryChunkViews
from pixel_battle.infrastructure.adapters.lock import FakeLock
from pixel_battle.infrastructure.adapters.offsets import InMemoryOffsets
from pixel_battle.presentation.scripts.update_chunk_view import (
    UpdateChunkView as Script,
)


@fixture
def script() -> Script:
    ok_file = StringIO()
    error_file = StringIO()

    interactor = Interactor(
        broker=InMemoryBroker(),
        lock=FakeLock(),
        default_chunk_view_where=DefaultCollectionChunkViewWhere(),
        chunk_views=InMemoryChunkViews(),
        offsets_of_latest_compressed_events=InMemoryOffsets(),
    )

    return Script(ok_file=ok_file, error_file=error_file, interactor=interactor)


async def test_ok(script: Script) -> None:
    argv[:] = ["_", "0", "0"]

    await script()

    output = script.ok_file.getvalue().split("\n")

    assert output[0] == "Updating..."
    assert output[1].startswith("The chunk view was updated. (")
    assert output[1].endswith(")")


@mark.parametrize(
    "args", (["0", "99"], ["-1", "0"], ["X", "0"], ["9"], ["--helps"])
)
async def test_with_invalid_args(script: Script, args: list[str]) -> None:
    argv[:] = ["_", *args]

    await script()

    output = script.error_file.getvalue()
    assert output == "Coordinates must be numbers in range(0, 10).\n"


async def test_help(script: Script) -> None:
    argv[:] = ["_", "--help"]

    await script()

    output = script.ok_file.getvalue()
    excepted_output = (
        "\nUsage:  python [script_path] [chunk_number_x] [chunk_number_y]"
        "\n\nCoordinates must be numbers in range(0, 10).\n"
    )

    assert output == excepted_output
