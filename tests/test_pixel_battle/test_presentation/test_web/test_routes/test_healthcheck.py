from fastapi import status
from httpx import AsyncClient
from pytest import mark


@mark.parametrize("stage", ["status_code", "body"])
async def test_ok(client: AsyncClient, stage: str) -> None:
    response = await client.get("/healthcheck")

    if stage == "status_code":
        assert response.status_code == status.HTTP_200_OK

    if stage == "body":
        assert response.json() == {}
