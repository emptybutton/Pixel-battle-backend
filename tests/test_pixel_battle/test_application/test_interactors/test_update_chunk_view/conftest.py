from pytest import fixture

from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black, red, white
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewOf,
)
from pixel_battle.infrastructure.adapters.chunk_views import InMemoryChunkViews
from pixel_battle.infrastructure.adapters.lock import FakeLock
from pixel_battle.infrastructure.adapters.offsets import InMemoryOffsets


@fixture
def update_chunk_view() -> UpdateChunkView[CollectionChunkView, int]:
    return UpdateChunkView(
        broker=InMemoryBroker(),
        lock=FakeLock(),
        default_chunk_view_of=DefaultCollectionChunkViewOf(),
        chunk_views=InMemoryChunkViews(),
        offsets_of_latest_compressed_events=InMemoryOffsets(),
    )


@fixture
def pixel1_1() -> Pixel[RGBColor]:
    return Pixel(color=white, position=Vector())


@fixture
def pixel1_2() -> Pixel[RGBColor]:
    return Pixel(color=black, position=Vector())


@fixture
def pixel2_1() -> Pixel[RGBColor]:
    return Pixel(color=black, position=Vector(x=50, y=60))


@fixture
def pixel2_2() -> Pixel[RGBColor]:
    return Pixel(color=white, position=Vector(x=50, y=60))


@fixture
def pixel3() -> Pixel[RGBColor]:
    return Pixel(color=red, position=Vector(x=99, y=99))


@fixture
def chunk() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


@fixture
def view1_2_and_2_1(
    pixel1_2: Pixel[RGBColor],
    pixel2_1: Pixel[RGBColor],
) -> CollectionChunkView:
    return CollectionChunkView([pixel1_2, pixel2_1])
