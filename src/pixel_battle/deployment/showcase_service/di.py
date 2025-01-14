from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    ProcessInfrastructureAdapterProvider,
    StreamingProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.healthchek import (
    router as healthchek_router,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)


class ShowcaseServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [
            healthchek_router,
            recolor_pixel_router,
            view_chunk_router,
            stream_chunk_router,
        ]

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    ProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    ShowcaseServiceProvider(),
    StreamingProvider(),
)
