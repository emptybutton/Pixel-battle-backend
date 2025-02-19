from asyncio import gather, sleep
from collections.abc import Awaitable
from typing import Callable

from pytest import fixture, mark

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    RGBColor,
    black,
    white,
)
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue


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
def queue() -> InMemoryPixelQueue:
    return InMemoryPixelQueue(pulling_timeout_seconds=0.001)


type Push = Callable[[Pixel[RGBColor]], Awaitable[None]]


@fixture
def push(queue: InMemoryPixelQueue) -> Push:
    async def func(pixel: Pixel[RGBColor]) -> None:
        await sleep(0.000_5)
        await queue.push(pixel)

    return func


async def test_push(
    queue: InMemoryPixelQueue,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor]
) -> None:
    await queue.push(pixel1)
    await queue.push(pixel2)

    assert dict(queue) == {pixel1.chunk: [pixel1, pixel2]}


@mark.parametrize(
    "is_commitable, only_new",
    [
        (False, False),
        (True, False),
        (True, True),
    ],
)
async def test_empty_queue_pulling(
    is_commitable: bool,
    only_new: bool,
    queue: InMemoryPixelQueue,
    push: Push,
    pixel1: Pixel[RGBColor],
) -> None:
    async def pull() -> tuple[Pixel[RGBColor], ...]:
        if is_commitable:
            async with queue.committable_pulled_pixels_when(
                chunk=pixel1.chunk, process=None, only_new=only_new
            ) as pixels:
                return pixels

        return await queue.uncommittable_pulled_pixels_when(
            chunk=pixel1.chunk, process=None
        )

    pixels, _ = await gather(pull(), push(pixel1))
    assert pixels == (pixel1, )


@mark.parametrize(
    "is_commitable, only_new",
    [
        (False, False),
        (True, False),
        (True, True),
    ],
)
async def test_full_queue_pulling(
    is_commitable: bool,
    only_new: bool,
    queue: InMemoryPixelQueue,
    push: Push,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
    pixel4: Pixel[RGBColor],
) -> None:
    await queue.push(pixel1)

    async def pull() -> tuple[Pixel[RGBColor], ...]:
        if is_commitable:
            async with queue.committable_pulled_pixels_when(
                chunk=pixel1.chunk, process=None, only_new=only_new
            ) as pixels:
                return pixels

        return await queue.uncommittable_pulled_pixels_when(
            chunk=pixel1.chunk, process=None
        )

    pixels, _ = await gather(pull(), push(pixel2))

    if is_commitable and only_new:
        assert pixels == (pixel2, )
    elif is_commitable and not only_new:
        assert pixels == (pixel1, )
    elif not is_commitable and only_new:
        assert pixels == (pixel2, )
    elif not is_commitable and not only_new:
        assert pixels == (pixel1, )

    await push(pixel3)
    pixels, _ = await gather(pull(), push(pixel4))

    if is_commitable and only_new:
        assert pixels == (pixel3, )
    elif is_commitable and not only_new:
        assert pixels == (pixel2, pixel3)
    elif not is_commitable and only_new:
        assert pixels == (pixel4, )
    elif not is_commitable and not only_new:
        assert pixels == (pixel1, pixel2, pixel3)

    pixels = await pull()

    if is_commitable and only_new:  # noqa: SIM114
        assert pixels == (pixel4, )
    elif is_commitable and not only_new:
        assert pixels == (pixel4, )
    elif not is_commitable and only_new:
        assert pixels == tuple()
    elif not is_commitable and not only_new:
        assert pixels == (pixel1, pixel2, pixel3, pixel4)
