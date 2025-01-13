from dishka import make_async_container

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    DistributedTaskProvider,
    InfrastructureProvider,
    InteractorProvider,
)


chunk_stream_compression_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    DistributedTaskProvider(),
)
