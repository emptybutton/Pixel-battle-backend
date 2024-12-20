from pytest import fixture
from redis.asyncio.cluster import RedisCluster

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.offsets import (
    InRedisClusterRedisStreamOffsets,
)
from pixel_battle.infrastructure.redis.types import RedisStreamOffset


@fixture
def offsets(redis_cluster: RedisCluster) -> InRedisClusterRedisStreamOffsets:
    return InRedisClusterRedisStreamOffsets(redis_cluster=redis_cluster)


@fixture
def offset() -> RedisStreamOffset:
    return b"0"


@fixture
def chunk() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


@fixture
def key() -> bytes:
    return bytes([ord("{"), 0, ord("}")])


@fixture
def field() -> bytes:
    return b"offset"


async def test_put(
    chunk: Chunk,
    redis_cluster: RedisCluster,
    offsets: InRedisClusterRedisStreamOffsets,
    offset: RedisStreamOffset,
    key: bytes,
    field: bytes,
) -> None:
    await redis_cluster.flushdb()

    await offsets.put(offset, chunk=chunk)

    stored_offset = await redis_cluster.hget(key, field)
    assert stored_offset == offset


async def test_offset_for_without_offset(
    chunk: Chunk,
    redis_cluster: RedisCluster,
    offsets: InRedisClusterRedisStreamOffsets,
    offset: RedisStreamOffset,
) -> None:
    await redis_cluster.flushdb()

    offset = await offsets.offset_for(chunk=chunk)

    assert offset is None


async def test_offset_for_with_offset(
    chunk: Chunk,
    redis_cluster: RedisCluster,
    offsets: InRedisClusterRedisStreamOffsets,
    offset: RedisStreamOffset,
    key: bytes,
    field: bytes,
) -> None:
    await redis_cluster.flushdb()
    await redis_cluster.hset(key, field, offset)

    stored_offset = await offsets.offset_for(chunk=chunk)

    assert stored_offset == offset
