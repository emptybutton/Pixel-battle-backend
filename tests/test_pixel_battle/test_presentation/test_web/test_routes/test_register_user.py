from fastapi import status
from httpx import AsyncClient, Cookies
from pytest import mark


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_ok(
    client: AsyncClient, stage: str
) -> None:
    response = await client.post("/pixel-battle/user")

    if stage == "status_code":
        assert response.status_code == status.HTTP_201_CREATED

    if stage == "body":
        assert response.json() == {}

    if stage == "cookies":
        assert set(response.cookies) == {"userData"}


@mark.parametrize("stage", ["status_code", "body"])
async def test_already_registered(
    client: AsyncClient, stage: str, cookies_with_right: Cookies
) -> None:
    client.cookies = cookies_with_right
    response = await client.post("/pixel-battle/user")

    if stage == "status_code":
        assert response.status_code == status.HTTP_403_FORBIDDEN

    if stage == "body":
        assert response.json() == {"errors": [{"type": "AlreadyRegistered"}]}
