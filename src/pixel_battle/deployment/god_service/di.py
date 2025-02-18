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
from pixel_battle.presentation.web.routers import all_routers
from pixel_battle.presentation.web.streaming import Streaming


class GodServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return all_routers

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
