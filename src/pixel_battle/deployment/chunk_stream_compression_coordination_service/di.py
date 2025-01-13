from dishka import make_async_container

from pixel_battle.deployment.common.di import (
    DistributedTaskProvider,
    InteractorProvider,
    OutOfProcessInfrastructureAdapterProvider,
    OutOfProcessInfrastructureProvider,
)


chunk_stream_compression_coordination_service_container = make_async_container(
    OutOfProcessInfrastructureProvider(),
    OutOfProcessInfrastructureAdapterProvider(),
    InteractorProvider(),
    DistributedTaskProvider(),
)
