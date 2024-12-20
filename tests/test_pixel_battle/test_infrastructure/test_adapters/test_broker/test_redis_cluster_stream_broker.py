from asyncio import gather, sleep

from pytest import fixture
from redis.asyncio.cluster import RedisCluster

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import (
    RGBColor,
    black,
    white,
)
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.broker import RedisClusterStreamBroker
from pixel_battle.infrastructure.encoding import decoded, encoded


@fixture
def broker(redis_cluster: RedisCluster) -> RedisClusterStreamBroker:
    return RedisClusterStreamBroker(redis_cluster=redis_cluster)


@fixture
def pixel1() -> Pixel[RGBColor]:
    return Pixel(position=Vector(x=50, y=0), color=white)


@fixture
def pixel2() -> Pixel[RGBColor]:
    return Pixel(position=Vector(x=50, y=0), color=black)


@fixture
def pixel3() -> Pixel[RGBColor]:
    return Pixel(position=Vector(x=99, y=99), color=white)


@fixture
def stream_key() -> bytes:
    return b"{" + bytes([0]) + b"}stream"


async def test_publish_event_with(
    broker: RedisCluster,
    redis_cluster: RedisCluster,
    stream_key: bytes,
    pixel1: Pixel[RGBColor],
) -> None:
    await redis_cluster.flushdb()

    await broker.publish_event_with(pixel=pixel1)

    events = await redis_cluster.xrange(stream_key)
    pixels = [
        decoded(event[1][bytes(0)], chunk=pixel1.chunk) for event in events
    ]

    assert pixels == [pixel1]


async def test_events_after(
    broker: RedisCluster,
    redis_cluster: RedisCluster,
    stream_key: bytes,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
) -> None:
    await redis_cluster.flushdb()

    offset = await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel1)})
    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel2)})
    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel3)})

    events = await broker.events_after(offset, chunk=pixel1.chunk)
    pixels = [event.pixel for event in events]

    assert pixels == [pixel2, pixel3]


async def test_new_events(
    broker: RedisCluster,
    redis_cluster: RedisCluster,
    stream_key: bytes,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
) -> None:
    async def pull_pixels() -> list[Pixel[RGBColor]]:
        async with broker.new_events_of(pixel1.chunk) as events:
            return [event.pixel for event in events]

    await redis_cluster.flushdb()

    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel1)})

    pixels = await pull_pixels()
    assert pixels == []

    async def xadd_pixel2() -> None:
        await sleep(0.2)
        await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel2)})

    _, pixels = await gather(xadd_pixel2(), pull_pixels())

    assert pixels == [pixel2]

    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel3)})

    pixels = await pull_pixels()
    assert pixels == [pixel3]


async def test_events_of(
    broker: RedisCluster,
    redis_cluster: RedisCluster,
    stream_key: bytes,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
) -> None:
    await redis_cluster.flushdb()

    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel1)})
    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel2)})
    await redis_cluster.xadd(stream_key, {bytes(0): encoded(pixel3)})

    events = await broker.events_of(pixel1.chunk)
    pixels = [event.pixel for event in events]

    assert pixels == [pixel1, pixel2, pixel3]
