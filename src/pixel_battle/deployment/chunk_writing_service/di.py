
from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    InfrastructureProvider,
    InteractorProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)


class ChunkWritingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [recolor_pixel_router]

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


chunk_writing_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ChunkWritingServiceProvider(),
)
