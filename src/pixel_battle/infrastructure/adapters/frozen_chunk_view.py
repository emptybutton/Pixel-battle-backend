
from pixel_battle.application.ports.frozen_chunk_view import ChunkViewFreezing
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.pillow.types import PillowPNGImageData


type FrozenCollectionChunkView = frozenset[Pixel[RGBColor]]


class CollectionChunkViewFreezing(
    ChunkViewFreezing[CollectionChunkView, FrozenCollectionChunkView]
):
    async def frozen(
        self, chunk_view: CollectionChunkView
    ) -> FrozenCollectionChunkView:
        return frozenset(chunk_view)


type FrozenPNGImageChunkView = PillowPNGImageData


class PNGImageChunkViewFreezing(
    ChunkViewFreezing[PNGImageChunkView, FrozenPNGImageChunkView]
):
    async def frozen(
        self, chunk_view: PNGImageChunkView
    ) -> FrozenPNGImageChunkView:
        return chunk_view.to_png_image_data()
