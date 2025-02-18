import asyncio
from collections.abc import AsyncIterator, Coroutine, Iterable
from contextlib import asynccontextmanager, suppress
from typing import Any, cast

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI

from pixel_battle.presentation.web.tags import tags_metadata


type AppCoroutines = Iterable[Coroutine[Any, Any, Any]]
type AppRouters = Iterable[APIRouter]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    with suppress(asyncio.CancelledError):
        async with asyncio.TaskGroup() as tasks:
            for coroutine in cast("AppCoroutines", app.state.coroutines):
                tasks.create_task(coroutine)

            yield

            await app.state.dishka_container.close()
            raise asyncio.CancelledError


async def app_from(container: AsyncContainer) -> FastAPI:
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
        openapi_tags=tags_metadata,
        contact={"name": "Alexander Smolin", "url": author_url},
        license_info={
            "name": "Apache 2.0",
            "url": f"{repo_url}/blob/main/LICENSE",
        },
        lifespan=lifespan,
    )

    coroutines = await container.get(AppCoroutines)
    routers = await container.get(AppRouters)

    app.state.coroutines = coroutines

    for router in routers:
        app.include_router(router)

    setup_dishka(container=container, app=app)

    return app
