from asyncio import gather, sleep

from pytest import fixture

from pixel_battle.application.ports.broker import NewPixelColorEvent
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import (
    RGBColor,
    black,
    white,
)
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker


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
def stored_pixels(
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
) -> tuple[Pixel[RGBColor], ...]:
    return (pixel1, pixel2)


@fixture
def unstored_pixel(pixel3: Pixel[RGBColor]) -> Pixel[RGBColor]:
    return pixel3


@fixture
def empty_broker() -> InMemoryBroker:
    return InMemoryBroker()


@fixture
def filled_broker(stored_pixels: tuple[Pixel[RGBColor], ...]) -> InMemoryBroker:
    return InMemoryBroker(stored_pixels)


async def test_push_event_with(
    empty_broker: InMemoryBroker, pixel1: Pixel[RGBColor]
) -> None:
    await empty_broker.push_event_with(pixel=pixel1)

    assert dict(empty_broker) == {pixel1.chunk: [pixel1]}


async def test_events_after(
    filled_broker: InMemoryBroker, stored_pixels: tuple[Pixel[RGBColor], ...]
) -> None:
    events = await filled_broker.events_after(0, chunk=stored_pixels[0].chunk)
    expected_events = (NewPixelColorEvent(pixel=stored_pixels[1], offset=1), )

    assert events == expected_events


async def test_events_when(
    filled_broker: InMemoryBroker, stored_pixels: tuple[Pixel[RGBColor], ...]
) -> None:
    events = await filled_broker.events_when(chunk=stored_pixels[0].chunk)
    expected_events = (
        NewPixelColorEvent(pixel=stored_pixels[0], offset=0),
        NewPixelColorEvent(pixel=stored_pixels[1], offset=1),
    )

    assert events == expected_events


async def test_pulled_events_when(
    empty_broker: InMemoryBroker,
    pixel1: Pixel[RGBColor],
    pixel2: Pixel[RGBColor],
    pixel3: Pixel[RGBColor],
) -> None:
    await empty_broker.push_event_with(pixel=pixel1)

    async def pull_events() -> tuple[NewPixelColorEvent[int], ...]:
        context = empty_broker.pulled_events_when(chunk=pixel1.chunk)
        async with context as events:
            return events

    async def push_event_with_pixel2() -> None:
        await sleep(0.2)
        await empty_broker.push_event_with(pixel=pixel2)

    events, _ = await gather(pull_events(), push_event_with_pixel2())

    expected_events = (NewPixelColorEvent(pixel=pixel2, offset=1), )
    assert events == expected_events

    await empty_broker.push_event_with(pixel=pixel3)
    events = await pull_events()

    expected_events = (NewPixelColorEvent(pixel=pixel3, offset=2), )
    assert events == expected_events
