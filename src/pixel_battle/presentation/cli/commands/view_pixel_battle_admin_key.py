import sys

from click import Abort, command, echo, option, style
from dishka import FromDishka

from pixel_battle.application.interactors.view_pixel_battle_admin_key import (
    Error,
    Ok,
    ViewPixelBattleAdminKey,
)


@command(name="admin-key")
@option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Write only an admin key",
)
async def view_pixel_battle_admin_key_command(
    view_pixel_battle_admin_key: FromDishka[ViewPixelBattleAdminKey],
    quiet: bool,
) -> None:
    result = await view_pixel_battle_admin_key()

    if quiet:
        if isinstance(result, Ok):
            echo(result.admin_key.token)
            return
        else:
            sys.exit(1)

    if result is Error.pixel_battle_is_not_initiated_error:
        echo("Pixel-Battle is not initiated.")
        sys.exit(1)

    styled_admin_key = style(result.admin_key.token, fg="cyan")
    echo(f"Your admin key: {styled_admin_key}")
