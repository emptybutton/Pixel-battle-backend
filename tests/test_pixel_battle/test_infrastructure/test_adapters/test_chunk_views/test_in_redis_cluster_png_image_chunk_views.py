from pytest import fixture
from redis.asyncio.cluster import RedisCluster

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.infrastructure.adapters.chunk_views import (
    InRedisClusterPNGImageChunkViews,
)


@fixture(scope="session")
def views(redis_cluster: RedisCluster) -> InRedisClusterPNGImageChunkViews:
    return InRedisClusterPNGImageChunkViews(
        redis_cluster=redis_cluster,
        close_when_putting=False,
    )


async def test_all_view_life_cycle(
    views: InRedisClusterPNGImageChunkViews,
    png_image_chunk_view1: PNGImageChunkView,
) -> None:
    chunk = Chunk(number=ChunkNumber(x=9, y=0))

    await views.put(png_image_chunk_view1, chunk=chunk)
    result_chunk_view = await views.chunk_view_where(chunk=chunk)

    assert result_chunk_view == png_image_chunk_view1


async def test_chunk_view_where_without_view(
    views: InRedisClusterPNGImageChunkViews,
    redis_cluster: RedisCluster,
) -> None:
    await redis_cluster.flushdb()

    chunk = Chunk(number=ChunkNumber(x=9, y=0))

    assert await views.chunk_view_where(chunk=chunk) is None
