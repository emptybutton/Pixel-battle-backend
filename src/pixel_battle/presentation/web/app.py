from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterable

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def app_with(
    *,
    container: AsyncContainer,
    routers: Iterable[APIRouter],
) -> FastAPI:
    author_url = "https://github.com/emptybutton"
    repo_url = f"{author_url}/Pixel-battle-backend"

    description = (
        "Pixel battle is an online game with open source code posted on"
        f" [github]({repo_url})."
    )
    app = FastAPI(
        title="PixelBattleAPI",
        version="0.1.0",
        summary="Pixel battle API for interaction via web browsers.",
        description=description,
        contact={"name": "Alexander Smolin", "url": author_url},
        license_info={
            "name": "Apache 2.0",
            "url": f"{repo_url}/blob/main/LICENSE",
        },
        lifespan=lifespan,
    )

    for router in routers:
        app.include_router(router)

    setup_dishka(container=container, app=app)

    return app
