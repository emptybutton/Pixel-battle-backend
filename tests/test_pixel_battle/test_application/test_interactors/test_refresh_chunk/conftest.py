from pytest import fixture

from pixel_battle.application.interactors.refresh_chunk import (
    RefreshChunk,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor, black, red, white
from pixel_battle.infrastructure.adapters.chunk_optimistic_lock import (
    AsyncIOChunkOptimisticLockWhen,
)
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewWhen,
)
from pixel_battle.infrastructure.adapters.chunk_views import InMemoryChunkViews
from pixel_battle.infrastructure.adapters.frozen_chunk_view import (
    CollectionChunkViewFreezing,
)
from pixel_battle.infrastructure.adapters.frozen_chunk_views import (
    InMemoryFrozenChunkViews,
)
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue


@fixture
def refresh_chunk() -> RefreshChunk[CollectionChunkView]:
    return RefreshChunk(
        pixel_queue=InMemoryPixelQueue(pulling_timeout_seconds=0),
        default_chunk_view_when=DefaultCollectionChunkViewWhen(),
        chunk_views=InMemoryChunkViews(),
        chunk_optimistic_lock_when=AsyncIOChunkOptimisticLockWhen(),
        frozen_chunk_views=InMemoryFrozenChunkViews(
            frozen_chunk_view_by_chunk=dict()
        ),
        chunk_view_freezing=CollectionChunkViewFreezing(),
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
