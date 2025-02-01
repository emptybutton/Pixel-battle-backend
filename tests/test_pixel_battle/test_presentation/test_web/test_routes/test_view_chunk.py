import json

from dishka import AsyncContainer
from fastapi import status
from httpx import AsyncClient
from PIL.Image import open
from pytest import mark

from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import black, red
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView


@mark.parametrize("stage", ["status_code", "body", "headers"])
async def test_ok(
    client: AsyncClient, stage: str, container: AsyncContainer
) -> None:
    async with container() as request_container:
        queue = await request_container.get(PixelQueue)

    await queue.push(Pixel(position=Vector(x=5), color=black))
    await queue.push(Pixel(position=Vector(y=5), color=red))

    response = await client.get("/canvas/chunk/0/0")

    if stage == "status_code":
        assert response.status_code == status.HTTP_200_OK

    if stage == "body":
        expected_body = PNGImageChunkView.create_default()
        body = PNGImageChunkView(open(response))  # type: ignore[arg-type]

        assert body == expected_body

    if stage == "headers":
        expected_delta_of_changes_header = {
            "pixels": [
                {"pixelPosition": [5, 0], "newPixelColor": [0, 0, 0]},
                {"pixelPosition": [0, 5], "newPixelColor": [255, 0, 0]},
            ]
        }
        delta_header = (
            json.loads(response.headers["X-Actualizing-Delta"])
        )

        assert delta_header == expected_delta_of_changes_header
