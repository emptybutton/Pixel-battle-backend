import asyncio

from pixel_battle.deployment.chunk_refresh_worker.di import container
from pixel_battle.presentation.distributed_tasks.refresh_chunk import (
    RefreshChunkTask,
)


async def main() -> None:
    task = await container.get(RefreshChunkTask)

    try:
        await task.start_pulling()
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
