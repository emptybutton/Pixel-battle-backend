from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    DistributedTaskProvider,
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
    StreamingProvider,
)
from pixel_battle.presentation.distributed_tasks.refresh_chunk import (
    RefreshChunkTask,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.healthcheck import (
    router as healthcheck_router,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.register_user import (
    router as register_user_router,
)
from pixel_battle.presentation.web.routes.schedule_pixel_battle import (
    router as schedule_pixel_battle_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)
from pixel_battle.presentation.web.routes.view_pixel_battle import (
    router as view_pixel_battle_router,
)
from pixel_battle.presentation.web.routes.view_user import (
    router as view_user_router,
)
from pixel_battle.presentation.web.streaming import Streaming


class GodServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [
            healthcheck_router,
            view_pixel_battle_router,
            schedule_pixel_battle_router,
            view_user_router,
            register_user_router,
            recolor_pixel_router,
            view_chunk_router,
            stream_chunk_router,
        ]

    @provide
    def provide_coroutines(
        self,
        streaming: Streaming,
        refresh_chunk_task: RefreshChunkTask,
    ) -> AppCoroutines:
        return [
            refresh_chunk_task.start_pulling(),
            refresh_chunk_task.start_pushing(),
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
