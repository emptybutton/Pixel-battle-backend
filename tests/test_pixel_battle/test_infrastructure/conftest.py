from typing import AsyncIterator, Iterator

from PIL.Image import open
from pytest import Item, fixture, mark
from pytest_asyncio import is_async_test
from redis.asyncio.cluster import RedisCluster

from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.infrastructure.env import Env


@fixture(scope="session")
async def redis_cluster() -> AsyncIterator[RedisCluster]:
    async with RedisCluster.from_url(Env.redis_cluster_url) as redis_cluster:
        yield redis_cluster


@fixture(scope="session")
def png_image_chunk_view1() -> Iterator[PNGImageChunkView]:
    """Has a blue pixel on (2, 1) and a white background."""

    with open("tests/test_pixel_battle/assets/chunk-view1.png") as image:
        yield PNGImageChunkView(image)


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
