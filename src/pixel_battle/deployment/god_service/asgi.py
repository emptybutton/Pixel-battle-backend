from pixel_battle.deployment.common.asgi import LazyASGIApp
from pixel_battle.deployment.god_service.di import container
from pixel_battle.presentation.web.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
