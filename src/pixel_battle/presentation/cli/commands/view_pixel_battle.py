import json

from click import Choice, command, echo, option, style
from dishka import FromDishka

from pixel_battle.application.interactors.view_pixel_battle import (
    Output,
    ViewPixelBattle,
)


@command()
@option(
    "-f",
    "--format",
    type=Choice(["default", "json", "short-json"]),
    default="default",
    help="Use format for output.",
)
async def view_pixel_battle_command(
    view_pixel_battle: FromDishka[ViewPixelBattle],
    format: str | None,
) -> None:
    result = await view_pixel_battle()

    if format == "default":
        _write_as_default(result)
    elif format == "json":
        _write_as_json(result, short=False)
    elif format == "short-json":
        _write_as_json(result, short=True)


def _write_as_default(output: Output) -> None:
    if output.pixel_battle_time_delta is not None:
        start_datetime = output.pixel_battle_time_delta.start_time.datetime
        end_datetime = output.pixel_battle_time_delta.end_time.datetime

        styled_start_datetime = style(start_datetime, "cyan")
        styled_end_datetime = style(end_datetime, "cyan")
    else:
        styled_start_datetime = style(None, "red")
        styled_end_datetime = style(None, "red")

    styled_is_going_on = style(output.is_pixel_battle_going_on, "yellow")

    echo(f"is_going_on: {styled_is_going_on}")
    echo(f"start_time: {styled_start_datetime}")
    echo(f"end_time: {styled_end_datetime}")


def _write_as_json(output: Output, *, short: bool) -> None:
    if output.pixel_battle_time_delta is not None:
        start_datetime = output.pixel_battle_time_delta.start_time.datetime
        end_datetime = output.pixel_battle_time_delta.end_time.datetime

        start_time = start_datetime.isoformat()
        end_time = end_datetime.isoformat()
    else:
        start_time = None
        end_time = None

    jsonable_data = {
        "isGoingOn": output.is_pixel_battle_going_on,
        "startTime": start_time,
        "endTime": end_time,
    }

    if not short:
        echo(json.dumps(jsonable_data, indent=2))
    else:
        echo(json.dumps(jsonable_data, separators=(",", ":")))
