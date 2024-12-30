import json

from dishka import AsyncContainer
from fastapi import status
from httpx import AsyncClient
from PIL.Image import open
from pytest import mark

from pixel_battle.application.ports.broker import Broker
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import black, red
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView


@mark.parametrize("stage", ["status_code", "body", "headers"])
async def test_ok(
    client: AsyncClient, stage: str, container: AsyncContainer
) -> None:
    async with container() as request_container:
        broker = await request_container.get(Broker[int])

    await broker.push_event_with(pixel=Pixel(position=Vector(x=5), color=black))
    await broker.push_event_with(pixel=Pixel(position=Vector(y=5), color=red))

    response = await client.get("/canvas/chunk/0/0")

    if stage == "status_code":
        assert response.status_code == status.HTTP_200_OK

    if stage == "body":
        expected_body = PNGImageChunkView.create_default()
        body = PNGImageChunkView(open(response))

        assert body == expected_body

    if stage == "headers":
        expected_extension_header = {
            "pixels": [
                {"pixelPosition": [5, 0], "newPixelColor": [0, 0, 0]},
                {"pixelPosition": [0, 5], "newPixelColor": [255, 0, 0]},
            ]
        }
        extension_header = json.loads(response.headers["extension"])

        assert extension_header == expected_extension_header
