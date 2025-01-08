from dataclasses import dataclass

from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from httpx import ASGITransport, AsyncClient

from pixel_battle.presentation.web.app import (
    AppCoroutines,
    AppRouters,
    app_from,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class X:
    x: int


router = APIRouter()


@router.get("/something")
@inject
async def endpoint(x: FromDishka[X]) -> Response:
    return JSONResponse({"x": x.x})


async def test_app_from() -> None:
    provider = Provider(scope=Scope.APP)
    provider.provide(lambda: X(x=4), provides=X)
    provider.provide(lambda: [router], provides=AppRouters)
    provider.provide(lambda: [], provides=AppCoroutines)
    container = make_async_container(provider)

    app = await app_from(container)

    client = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    )
    async with client:
        response = await client.get("/something")
        output_json = response.json()

        assert output_json == {"x": 4}
