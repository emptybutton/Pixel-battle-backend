from dishka import make_async_container

from pixel_battle.deployment.common.di import (
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
    ScriptProvider,
)


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    ScriptProvider(),
)
