import sys
from datetime import UTC, datetime

from click import DateTime, command, echo, option, style
from dishka import FromDishka

from pixel_battle.application.interactors.initiate_pixel_battle import (
    InitiatePixelBattle,
)
from pixel_battle.entities.core.pixel_battle import (
    PixelBattleIsAlreadyInitiatedError,
)


@command(name="initiate")
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
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Write only an admin key",
)
async def initiate_pixel_battle_command(
    initiate_pixel_battle: FromDishka[InitiatePixelBattle],
    pixel_battle_start_time: datetime,
    pixel_battle_end_time: datetime,
    quiet: bool,
) -> None:
    start_time = datetime.now()

    try:
        result = await initiate_pixel_battle(
            pixel_battle_start_time.astimezone(UTC),
            pixel_battle_end_time.astimezone(UTC),
        )
    except PixelBattleIsAlreadyInitiatedError:
        if not quiet:
            echo("Pixel-Battle is already initiated.")

        sys.exit(1)

    end_time = datetime.now()
    time_delta = end_time - start_time
    delta_seconds = time_delta.total_seconds()

    if not quiet:
        styled_delta_seconds = style(delta_seconds, fg="cyan")
        styled_admin_key = style(
            result.pixel_battle.admin_key.token, fg="cyan"
        )
        echo(f"Pixel-Battle was initiated in {styled_delta_seconds} seconds.")
        echo(f"Your admin key: {styled_admin_key}")
    else:
        echo(result.pixel_battle.admin_key.token)
