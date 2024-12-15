from typing import Iterator

from PIL.Image import open
from pytest import fixture

from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView


@fixture(scope="session")
def png_image_chunk_view1() -> Iterator[PNGImageChunkView]:
    """Has a blue pixel on (2, 1) and a white background."""

    with open("tests/test_pixel_battle/assets/chunk-view1.png") as image:
        yield PNGImageChunkView(image)
