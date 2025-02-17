from itertools import product

from click import Command
from click.testing import CliRunner
from dishka import AsyncContainer
from pytest import fixture, mark

from pixel_battle.presentation.cli.commands.refresh_chunk import (
    refresh_chunk_command,
)
from pixel_battle.presentation.cli.dishka_integration import (
    command_with_injected_dependencies_when,
)


@fixture
def command(container: AsyncContainer) -> Command:
    return command_with_injected_dependencies_when(
        command=refresh_chunk_command,
        container=container,
    )


@fixture
def runner() -> CliRunner:
    return CliRunner()


@mark.parametrize(
    "data_injection, subject",
    product(
        ["short_options", "long_options", "stdin"],
        ["exit_code", "output"],
    ),
)
def test_not_quiet(
    runner: CliRunner,
    command: Command,
    data_injection: str,
    subject: str,
) -> None:
    if data_injection == "short_options":
        args = ["-x", "0", "-y", "0"]
        result = runner.invoke(command, args)

    elif data_injection == "long_options":
        args = ["--chunk-number-x", "0", "--chunk-number-y", "0"]
        result = runner.invoke(command, args)

    elif data_injection == "stdin":
        input_ = "0\n0"
        result = runner.invoke(command, input=input_)

    if subject == "exit_code":
        assert result.exit_code == 0

    if subject == "output" and data_injection != "stdin":
        assert result.output.startswith("The chunk image was refreshed in ")
        assert result.output.endswith(" seconds.\n")

    if subject == "output" and data_injection == "stdin":
        assert result.output.startswith(
            "chunk.number.x: 0"
            "\nchunk.number.y: 0"
            "\nThe chunk image was refreshed in "
        )
        assert result.output.endswith(" seconds.\n")


@mark.parametrize(
    "data_injection, subject",
    product(
        ["short_options", "long_options", "stdin"],
        ["exit_code", "output"],
    ),
)
def test_quiet(
    runner: CliRunner,
    command: Command,
    data_injection: str,
    subject: str,
) -> None:
    if data_injection == "short_options":
        args = ["-x", "0", "-y", "0", "-q"]
        result = runner.invoke(command, args)

    elif data_injection == "long_options":
        args = ["--chunk-number-x", "0", "--chunk-number-y", "0", "-q"]
        result = runner.invoke(command, args)

    elif data_injection == "stdin":
        args = ["-q"]
        input_ = "0\n0"
        result = runner.invoke(command, args, input_)

    if subject == "exit_code":
        assert result.exit_code == 0

    if subject == "output" and data_injection != "stdin":
        assert not result.output

    if subject == "output" and data_injection == "stdin":
        assert result.output == "chunk.number.x: 0\nchunk.number.y: 0\n"
