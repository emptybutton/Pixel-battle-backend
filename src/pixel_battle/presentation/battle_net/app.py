from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from pixel_battle.presentation.battle_net.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def app_with(container: AsyncContainer) -> FastAPI:
    author_url = "https://github.com/emptybutton"
    repo_url = f"{author_url}/Pixel-battle-backend"

    description = (
        "BattleNet is one of the APIs of the Pixel battle game, presented as a"
        " separate service responsible for creating communication channels"
        " between groups of clients to synchronize them in a cheap way."
        " \n\nPixel battle has open source code, which can be"
        f" found [here]({repo_url}) (including the code for this service)."
    )
    app = FastAPI(
        title="BattleNet",
        version="0.1.0",
        summary="Pixel battle API for client synchronization.",
        description=description,
        contact={"name": "Alexander Smolin", "url": author_url},
        license_info={
            "name": "Apache 2.0",
            "url": f"{repo_url}/blob/main/LICENSE",
        },
        lifespan=lifespan,
    )

    app.include_router(router)
    setup_dishka(container=container, app=app)

    return app
