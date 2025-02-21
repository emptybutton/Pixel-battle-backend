from asyncio import gather, sleep
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence

from pytest import fixture, mark
from redis.asyncio import RedisCluster

from pixel_battle.application.ports.pixel_queue import PullingProcess
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    RGBColor,
    black,
    white,
)
from pixel_battle.infrastructure.adapters.pixel_queue import (
    RedisClusterStreamPixelQueue,
)
from pixel_battle.infrastructure.encoding import (
    decoded_pixel_when,
    encoded_pixel_when,
)
from pixel_battle.infrastructure.redis.types import RedisStreamKey


@fixture(autouse=True, scope="function")
async def flushdb(redis_cluster: RedisCluster) -> AsyncIterator[None]:
    await redis_cluster.flushdb()
    yield


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
def pixel4() -> Pixel[RGBColor]:
    return Pixel(position=Vector(x=99, y=99), color=black)


@fixture
def queue(redis_cluster: RedisCluster) -> RedisClusterStreamPixelQueue:
    return RedisClusterStreamPixelQueue(
        redis_cluster=redis_cluster,
        pulling_timeout_seconds=0.5,
        max_stream_lenght=5_000_000,
    )


@fixture
def stream_key() -> RedisStreamKey:
    return b"{" + bytes([0]) + b"}_stream"


type Push = Callable[[Pixel[RGBColor]], Awaitable[None]]


@fixture
def push(redis_cluster: RedisCluster, stream_key: RedisStreamKey) -> Push:
    async def func(pixel: Pixel[RGBColor]) -> None:
        await sleep(0.05)

        body = encoded_pixel_when(pixel=pixel)
        await redis_cluster.xadd(stream_key, {bytes(0): body})

    return func


async def test_push(
    queue: RedisClusterStreamPixelQueue,
    redis_cluster: RedisCluster,
    stream_key: RedisStreamKey,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor]
) -> None:
    await queue.push(pixel1)
    await queue.push(pixel2)

    events = await redis_cluster.xrange(stream_key)
    pixels = [
        decoded_pixel_when(encoded_pixel=event[1][bytes(0)], chunk=pixel1.chunk)
        for event in events
    ]

    assert pixels == [pixel1, pixel2]


@mark.parametrize(
    "is_commitable, only_new, process",
    [
        (False, False, None),
        (True, False, None),
        (True, True, None),
        (False, False, PullingProcess.chunk_view_refresh),
        (True, False, PullingProcess.chunk_view_refresh),
        (True, True, PullingProcess.chunk_view_refresh),
    ],
)
async def test_empty_queue_pulling(
    is_commitable: bool,
    only_new: bool,
    process: PullingProcess | None,
    queue: RedisClusterStreamPixelQueue,
    push: Push,
    pixel1: Pixel[RGBColor],
) -> None:
    async def pull() -> Sequence[Pixel[RGBColor]]:
        if is_commitable:
            async with queue.committable_pulled_pixels_when(
                chunk=pixel1.chunk, process=process, only_new=only_new
            ) as pixels:
                return pixels

        return await queue.uncommittable_pulled_pixels_when(
            chunk=pixel1.chunk, process=process
        )

    pixels, _ = await gather(pull(), push(pixel1))
    assert pixels == (pixel1, )


@mark.parametrize(
    "is_commitable, only_new, process",
    [
        (False, False, None),
        (True, False, None),
        (True, True, None),
        (False, False, PullingProcess.chunk_view_refresh),
        (True, False, PullingProcess.chunk_view_refresh),
        (True, True, PullingProcess.chunk_view_refresh),
    ],
)
async def test_full_queue_pulling(
    is_commitable: bool,
    only_new: bool,
    process: PullingProcess | None,
    queue: RedisClusterStreamPixelQueue,
    push: Push,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
    pixel4: Pixel[RGBColor],
) -> None:
    await queue.push(pixel1)

    async def pull() -> Sequence[Pixel[RGBColor]]:
        if is_commitable:
            async with queue.committable_pulled_pixels_when(
                chunk=pixel1.chunk, process=process, only_new=only_new
            ) as pixels:
                return pixels

        return await queue.uncommittable_pulled_pixels_when(
            chunk=pixel1.chunk, process=process
        )

    pixels, _ = await gather(pull(), push(pixel2))

    if is_commitable and only_new:
        assert pixels == (pixel2, )
    elif is_commitable and not only_new:  # noqa: SIM114
        assert pixels == (pixel1, )
    elif not is_commitable:
        assert pixels == (pixel1, )

    await push(pixel3)
    pixels, _ = await gather(pull(), push(pixel4))

    if is_commitable and only_new:
        assert pixels == (pixel3, )
    elif is_commitable and not only_new:
        assert pixels == (pixel2, pixel3)
    elif not is_commitable:
        assert pixels == (pixel1, pixel2, pixel3)

    pixels = await pull()

    if is_commitable and only_new:  # noqa: SIM114
        assert pixels == (pixel4, )
    elif is_commitable and not only_new:
        assert pixels == (pixel4, )
    elif not is_commitable:
        assert pixels == (pixel1, pixel2, pixel3, pixel4)


@mark.parametrize("process", [None, PullingProcess.chunk_view_refresh])
async def test_commitable_only_new_pixels_added_outside_pulling(
    process: PullingProcess | None,
    queue: RedisClusterStreamPixelQueue,
    push: Push,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
) -> None:
    async def pull() -> Sequence[Pixel[RGBColor]]:
        async with queue.committable_pulled_pixels_when(
            chunk=pixel1.chunk, process=process, only_new=True
        ) as pixels:
            return pixels

    await push(pixel1)
    pixels = await pull()
    assert pixels == tuple()

    await push(pixel2)
    pixels = await pull()
    assert pixels == (pixel2, )

    await push(pixel3)
    pixels = await pull()
    assert pixels == (pixel3, )
