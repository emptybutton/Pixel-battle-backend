from dishka import make_async_container

from pixel_battle.deployments.common.di.providers import (
    AdapterProvider,
    ChunkReadingServiceProvider,
    ChunkStreamingServiceProvider,
    ChunkWritingServiceProvider,
    DistributedTaskProvider,
    GodServiceProvider,
    InfrastructureProvider,
    InteractorProvider,
    ScriptProvider,
    StreamingProvider,
)


chunk_writing_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ChunkWritingServiceProvider(),
)

chunk_reading_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ChunkReadingServiceProvider(),
)

chunk_streaming_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    StreamingProvider(),
    ChunkStreamingServiceProvider(),
)

chunk_stream_compression_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    DistributedTaskProvider(),
)

chunk_stream_compression_coordination_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    DistributedTaskProvider(),
)

god_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    GodServiceProvider(),
    StreamingProvider(),
    ChunkStreamingServiceProvider(),
    DistributedTaskProvider(),
)

compression_script_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ScriptProvider(),
)
