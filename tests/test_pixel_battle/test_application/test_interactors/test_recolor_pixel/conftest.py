from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, black
from pixel_battle.entities.quantities.position import zero_position
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    DefaultCollectionChunkViewOf,
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.transaction import (
    InMemoryChunkViewsTransactionOf,
)


@fixture
def recolor_pixel() -> RecolorPixel[CollectionChunkView]:
    return RecolorPixel[CollectionChunkView](
        chunk_views=InMemoryChunkViews(),
        transaction_of=InMemoryChunkViewsTransactionOf(),
        default_chunk_view_of=DefaultCollectionChunkViewOf(),
    )


@fixture
async def stored_pixel(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> Pixel[RGBColor]:
    pixel = Pixel(position=zero_position, color=black)
    view = CollectionChunkView([pixel])

    await recolor_pixel.chunk_views.put(view, chunk=pixel.chunk)

    return pixel
