from pixel_battle.deployment.admin_cli.di import container
from pixel_battle.presentation.cli.dishka import (
    command_with_injected_dependencies_when,
)
from pixel_battle.presentation.cli.groups import admin_group


def main() -> None:
    cli = command_with_injected_dependencies_when(
        container=container, command=admin_group,
    )
    cli()


if __name__ == "__main__":
    main()
