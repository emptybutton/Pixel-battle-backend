from pytest import fixture, raises

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import black
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.transaction import (
    InMemoryChunkViewsTransaction,
)


@fixture
def chunk() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


@fixture
def chunk_view() -> CollectionChunkView:
    return CollectionChunkView([
        Pixel(position=Vector(x=0, y=0), color=black),
        Pixel(position=Vector(x=50, y=50), color=black),
        Pixel(position=Vector(x=75, y=75), color=black)
    ])


async def test_without_error(
    chunk: Chunk, chunk_view: CollectionChunkView
) -> None:
    views = InMemoryChunkViews()

    async with InMemoryChunkViewsTransaction(views):
        await views.put(chunk_view, chunk=chunk)

    assert views.to_dict() == {chunk: chunk_view}


class _TestError(Exception): ...


async def test_with_error(
    chunk: Chunk, chunk_view: CollectionChunkView
) -> None:
    views = InMemoryChunkViews()

    with raises(_TestError):
        async with InMemoryChunkViewsTransaction(views):
            await views.put(chunk_view, chunk=chunk)
            raise _TestError

    assert views.to_dict() == dict()
