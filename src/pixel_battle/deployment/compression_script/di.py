from dishka import make_async_container

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    InfrastructureProvider,
    InteractorProvider,
    ScriptProvider,
)


compression_script_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ScriptProvider(),
)
