import asyncio

import uvicorn

from pixel_battle.deployment.god_service.di import god_service_container
from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewTask,
)
from pixel_battle.presentation.web.app import app_from
from pixel_battle.presentation.web.streaming import Streaming


async def run_app() -> None:
    app = await app_from(god_service_container)
    uvicorn.run(app)


async def main() -> None:
    streaming = await god_service_container.get(Streaming)
    update_chunk_view_task = await god_service_container.get(
        UpdateChunkViewTask
    )

    await asyncio.gather(
        run_app(),
        update_chunk_view_task.pull(),
        update_chunk_view_task.push(),
        streaming.start(),
    )


if __name__ == "__main__":
    asyncio.run(main())
