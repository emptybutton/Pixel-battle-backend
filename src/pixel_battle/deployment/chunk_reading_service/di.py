from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routers import ordered
from pixel_battle.presentation.web.routes.healthcheck import (
    healthcheck_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    view_chunk_router,
)


class ChunkReadingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return ordered(healthcheck_router, view_chunk_router)

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    ChunkReadingServiceProvider(),
)
