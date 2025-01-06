from asyncio import sleep

from httpx import AsyncClient
from httpx_ws import aconnect_ws


async def test_ok(client: AsyncClient) -> None:
    async with aconnect_ws("/canvas/chunk/0/0", client):
        await sleep(0.5)
