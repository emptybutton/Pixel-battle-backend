from pixel_battle.deployment.chunk_image_refresh_script.di import container
from pixel_battle.presentation.cli.commands.refresh_chunk_image import (
    refresh_chunk_image_command,
)
from pixel_battle.presentation.cli.dishka import (
    command_with_injected_dependencies_when,
)


def main() -> None:
    command = command_with_injected_dependencies_when(
        container=container,
        command=refresh_chunk_image_command,
    )
    command()


if __name__ == "__main__":
    main()
