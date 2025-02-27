from dishka import make_async_container

from pixel_battle.deployment.common.di import (
    DistributedTaskProvider,
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
)


container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    DistributedTaskProvider(),
)
