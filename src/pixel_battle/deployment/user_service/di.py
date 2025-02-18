from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routers import ordered
from pixel_battle.presentation.web.routes.register_user import (
    register_user_router,
)
from pixel_battle.presentation.web.routes.view_user import view_user_router


class UserServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return ordered(
            view_user_router,
            register_user_router
        )

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    UserServiceProvider(),
)
