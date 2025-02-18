from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routers import ordered
from pixel_battle.presentation.web.routes.schedule_pixel_battle import (
    schedule_pixel_battle_router,
)
from pixel_battle.presentation.web.routes.view_pixel_battle import (
    view_pixel_battle_router,
)


class AdminServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return ordered(
            view_pixel_battle_router,
            schedule_pixel_battle_router,
        )

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    AdminServiceProvider(),
)
