from pixel_battle.deployment.chunk_streaming_service.di import (
    chunk_streaming_service_container,
)
from pixel_battle.deployment.common.asgi import ASGIApp, LazyASGIApp
from pixel_battle.presentation.web.app import app_from


async def app_factory() -> ASGIApp:
    return await app_from(chunk_streaming_service_container)


app = LazyASGIApp(factory=app_factory)
