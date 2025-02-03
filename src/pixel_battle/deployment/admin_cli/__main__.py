from click import Group

from pixel_battle.deployment.admin_cli.di import container
from pixel_battle.presentation.cli.commands.initiate_pixel_battle import (
    initiate_pixel_battle_command,
)
from pixel_battle.presentation.cli.commands.refresh_chunk_image import (
    refresh_chunk_image_command,
)
from pixel_battle.presentation.cli.commands.view_pixel_battle_admin_key import (
    view_pixel_battle_admin_key_command,
)
from pixel_battle.presentation.cli.dishka import (
    command_with_injected_dependencies_when,
)


def main() -> None:
    root_group = Group()

    root_group.add_command(command_with_injected_dependencies_when(
        container=container, command=initiate_pixel_battle_command,
    ))
    root_group.add_command(command_with_injected_dependencies_when(
        container=container, command=view_pixel_battle_admin_key_command,
    ))

    chunk_group = Group(name="chunk")
    chunk_group.add_command(command_with_injected_dependencies_when(
        container=container,
        command=refresh_chunk_image_command,
    ))
    root_group.add_command(chunk_group)

    root_group()


if __name__ == "__main__":
    main()
