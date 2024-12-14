from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.chunk_view import CollectionChunkView


async def test_result(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    output = await recolor_pixel(
        user_id=None,
        datetime_of_user_obtaining_recoloring_right=None,
        pixel_position_x=0,
        pixel_position_y=0,
        chunk_number_x=0,
        chunk_number_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert output.pixel is None
    assert output.user.chunk == Chunk(number=ChunkNumber(x=0, y=0))


async def test_chunk_views(
    recolor_pixel: RecolorPixel[CollectionChunkView]
) -> None:
    await recolor_pixel(
        user_id=None,
        datetime_of_user_obtaining_recoloring_right=None,
        pixel_position_x=0,
        pixel_position_y=0,
        chunk_number_x=0,
        chunk_number_y=0,
        new_color_red_value_number=255,
        new_color_green_value_number=255,
        new_color_blue_value_number=255,
    )

    assert not recolor_pixel.chunk_views
