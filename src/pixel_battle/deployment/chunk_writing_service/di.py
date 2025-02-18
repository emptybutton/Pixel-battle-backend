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
from pixel_battle.presentation.web.routes.recolor_pixel import (
    recolor_pixel_router,
)


class ChunkWritingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return ordered(
            healthcheck_router,
            recolor_pixel_router,
        )

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    ChunkWritingServiceProvider(),
)
