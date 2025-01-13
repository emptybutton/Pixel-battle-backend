import asyncio

from pixel_battle.deployment.chunk_stream_compression_service.di import (
    chunk_stream_compression_service_container,
)
from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewTask,
)


async def main() -> None:
    task = await chunk_stream_compression_service_container.get(
        UpdateChunkViewTask
    )

    try:
        await task.start_pulling()
    finally:
        await chunk_stream_compression_service_container.close()


if __name__ == "__main__":
    asyncio.run(main())
