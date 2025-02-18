import sys
from datetime import UTC, datetime

from click import DateTime, command, echo, option, style
from dishka import FromDishka

from pixel_battle.application.interactors.schedule_pixel_battle import (
    SchedulePixelBattle,
)
from pixel_battle.entities.core.pixel_battle import (
    NotAuthorizedToScheduleError,
)
from pixel_battle.entities.space.time_delta import StartAfterEndTimeDeltaError


@command()
@option(
    "-s",
    "--pixel-battle-start-time",
    type=DateTime(),
    prompt="pixel_battle.start_time",
)
@option(
    "-e",
    "--pixel-battle-end-time",
    type=DateTime(),
    prompt="pixel_battle.end_time",
)
@option(
    "-k",
    "--admin-key",
    envvar="ADMIN_KEY",
    type=str,
    prompt="admin_key",
    show_envvar=True
)
@option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Don't write to stdout",
)
async def schedule_pixel_battle_command(
    schedule_pixel_battle: FromDishka[SchedulePixelBattle],
    pixel_battle_start_time: datetime,
    pixel_battle_end_time: datetime,
    admin_key: str,
    quiet: bool,
) -> None:
    start_time = datetime.now()

    try:
        await schedule_pixel_battle(
            pixel_battle_start_time.astimezone(UTC),
            pixel_battle_end_time.astimezone(UTC),
            admin_key,
        )
    except NotAuthorizedToScheduleError:
        if not quiet:
            echo(style("Forbidden.", bg="red"))

        sys.exit(1)
    except StartAfterEndTimeDeltaError:
        if not quiet:
            echo(style("Start after end.", bg="red"))

        sys.exit(1)

    end_time = datetime.now()
    time_delta = end_time - start_time
    delta_seconds = time_delta.total_seconds()

    if not quiet:
        styled_delta_seconds = style(delta_seconds, fg="cyan")
        echo(f"Pixel-Battle was scheduled in {styled_delta_seconds} seconds.")
