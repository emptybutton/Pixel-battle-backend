from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    DistributedTaskProvider,
    InfrastructureProvider,
    InteractorProvider,
    StreamingProvider,
)
from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewTask,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)
from pixel_battle.presentation.web.streaming import Streaming


class GodServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [recolor_pixel_router, view_chunk_router, stream_chunk_router]

    @provide
    def provide_coroutines(
        self,
        streaming: Streaming,
        update_chunk_view_task: UpdateChunkViewTask,
    ) -> AppCoroutines:
        return [
            update_chunk_view_task.pull(),
            update_chunk_view_task.push(),
            streaming.start(),
        ]


god_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    GodServiceProvider(),
    StreamingProvider(),
    DistributedTaskProvider(),
)
