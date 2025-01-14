from pixel_battle.deployment.chunk_reading_service.di import container
from pixel_battle.deployment.common.asgi import ASGIApp, LazyASGIApp
from pixel_battle.presentation.web.app import app_from


async def app_factory() -> ASGIApp:
    return await app_from(container)


app = LazyASGIApp(factory=app_factory)
