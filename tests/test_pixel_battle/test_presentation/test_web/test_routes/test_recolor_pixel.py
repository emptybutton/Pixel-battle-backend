from fastapi import status
from httpx import AsyncClient, Cookies
from pytest import mark


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_ok(
    client: AsyncClient, stage: str, cookies_with_right: Cookies
) -> None:
    input_json = {
        "pixelPosition": [0, 0],
        "newPixelColor": [255, 0, 0],
    }
    client.cookies = cookies_with_right
    response = await client.patch("/canvas", json=input_json)

    if stage == "status_code":
        assert response.status_code == status.HTTP_200_OK

    if stage == "body":
        assert response.json() == {}

    if stage == "cookies":
        assert set(response.cookies) == {"userData"}


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_pixel_out_of_canvas(
    client: AsyncClient, stage: str, cookies_with_right: Cookies
) -> None:
    input_json = {
        "pixelPosition": [-5, 0],
        "newPixelColor": [255, 0, 0],
    }
    client.cookies = cookies_with_right
    response = await client.patch("/canvas", json=input_json)

    if stage == "status_code":
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    if stage == "body":
        assert response.json() == {"errors": [{"type": "pixelOutOfCanvas"}]}

    if stage == "cookies":
        assert set(response.cookies) == set()


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_invalid_color_value_range(
    client: AsyncClient, stage: str, cookies_with_right: Cookies
) -> None:
    input_json = {
        "pixelPosition": [0, 0],
        "newPixelColor": [256, 0, 0],
    }
    client.cookies = cookies_with_right
    response = await client.patch("/canvas", json=input_json)

    if stage == "status_code":
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    if stage == "body":
        output_json = response.json()
        assert output_json == {"errors": [{"type": "invalidColorValueRange"}]}

    if stage == "cookies":
        assert set(response.cookies) == set()


@mark.parametrize("stage", ["status_code", "body", "cookies"])
async def test_no_right(
    client: AsyncClient, stage: str
) -> None:
    input_json = {
        "pixelPosition": [0, 0],
        "newPixelColor": [255, 0, 0],
    }
    response = await client.patch("/canvas", json=input_json)

    if stage == "status_code":
        assert response.status_code == status.HTTP_403_FORBIDDEN

    if stage == "body":
        output_json = response.json()
        assert output_json == {"errors": [{"type": "noRight"}]}

    if stage == "cookies":
        assert set(response.cookies) == set()
