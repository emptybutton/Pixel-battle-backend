from collections.abc import AsyncIterator, Iterator

from PIL.Image import open
from pytest import fixture
from redis.asyncio.cluster import RedisCluster

from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.infrastructure.envs import Envs


@fixture(scope="session")
async def redis_cluster(envs: Envs) -> AsyncIterator[RedisCluster]:
    cluster = RedisCluster.from_url(envs.canvas_redis_cluster_url)

    async with cluster:
        yield cluster


@fixture(scope="session")
def envs() -> Envs:
    return Envs.load()


@fixture(scope="session")
def png_image_chunk_view1() -> Iterator[PNGImageChunkView]:
    """Has a blue pixel on (2, 1) and a white background."""

    with open("tests/test_pixel_battle/assets/chunk-view1.png") as image:
        yield PNGImageChunkView(image)
