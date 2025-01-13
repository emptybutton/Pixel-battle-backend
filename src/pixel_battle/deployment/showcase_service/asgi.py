from pixel_battle.deployment.common.asgi import ASGIApp, LazyASGIApp
from pixel_battle.deployment.showcase_service.di import (
    showcase_service_container,
)
from pixel_battle.presentation.web.app import app_from


async def app_factory() -> ASGIApp:
    return await app_from(showcase_service_container)


app = LazyASGIApp(factory=app_factory)
