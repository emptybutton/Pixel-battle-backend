from typing import Iterable

from dishka import Provider, Scope, make_async_container, provide
from fastapi import APIRouter

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    DistributedTaskProvider,
    InfrastructureProvider,
    InteractorProvider,
    StreamingProvider,
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


class GodServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> Iterable[APIRouter]:
        return [recolor_pixel_router, view_chunk_router, stream_chunk_router]


god_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    GodServiceProvider(),
    StreamingProvider(),
    DistributedTaskProvider(),
)
