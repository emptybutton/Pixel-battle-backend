import asyncio

from pixel_battle.deployment.chunk_image_refresh_script.di import container
from pixel_battle.presentation.scripts.refresh_chunk_image import (
    RefreshChunkImageScript,
)


async def main() -> None:
    script = await container.get(RefreshChunkImageScript)

    try:
        await script()
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
