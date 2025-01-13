import asyncio

from pixel_battle.deployment.compression_script.di import (
    compression_script_container,
)
from pixel_battle.presentation.scripts.update_chunk_view import (
    UpdateChunkViewScript,
)


async def main() -> None:
    script = await compression_script_container.get(UpdateChunkViewScript)

    try:
        await script()
    finally:
        await compression_script_container.close()


if __name__ == "__main__":
    asyncio.run(main())
