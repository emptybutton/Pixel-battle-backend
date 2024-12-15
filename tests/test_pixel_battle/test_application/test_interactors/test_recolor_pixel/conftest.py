from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black
from pixel_battle.entities.quantities.vector import Vector
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewOf,
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.lock import (
    AsyncIOLock,
)


@fixture
def recolor_pixel() -> RecolorPixel[CollectionChunkView]:
    return RecolorPixel[CollectionChunkView](
        chunk_views=InMemoryChunkViews(),
        default_chunk_view_of=DefaultCollectionChunkViewOf(),
        lock=AsyncIOLock(),
    )


@fixture
async def stored_pixel(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> Pixel[RGBColor]:
    pixel = Pixel(position=Vector(), color=black)
    view = CollectionChunkView([pixel])

    await recolor_pixel.chunk_views.put(view, chunk=pixel.chunk)

    return pixel
