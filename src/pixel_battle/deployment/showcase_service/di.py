from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    ProcessInfrastructureAdapterProvider,
    StreamingProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routers import all_routers


class ShowcaseServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return all_routers

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


container = make_async_container(
    ProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    ShowcaseServiceProvider(),
    StreamingProvider(),
)
