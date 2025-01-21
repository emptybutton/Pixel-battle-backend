from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    DistributedTaskProvider,
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
    StreamingProvider,
)
from pixel_battle.presentation.distributed_tasks.refresh_chunk_view import (
    RefreshChunkViewTask,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.healthchek import (
    router as healthchek_router,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.register_user import (
    router as register_user_router,
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
        return [
            healthchek_router,
            recolor_pixel_router,
            view_chunk_router,
            stream_chunk_router,
            register_user_router,
        ]

    @provide
    def provide_coroutines(
        self,
        streaming: Streaming,
        refresh_chunk_view_task: RefreshChunkViewTask,
    ) -> AppCoroutines:
        return [
            refresh_chunk_view_task.start_pulling(),
            refresh_chunk_view_task.start_pushing(),
            streaming.start(),
        ]


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    GodServiceProvider(),
    StreamingProvider(),
    DistributedTaskProvider(),
)
