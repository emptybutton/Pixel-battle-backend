import asyncio

from pixel_battle.deployment.chunk_image_refresh_worker.di import container
from pixel_battle.presentation.distributed_tasks.refresh_chunk_view import (
    RefreshChunkViewTask,
)


async def main() -> None:
    task = await container.get(RefreshChunkViewTask)

    try:
        await task.start_pulling()
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
