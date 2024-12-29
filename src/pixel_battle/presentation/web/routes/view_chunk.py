from typing import Any

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from fastapi.responses import Response

from pixel_battle.application.interactors.view_chunk import ViewChunk
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema


router = APIRouter()


@router.get("/canvas/chunk/{chunk_number_x}/{chunk_number_y}")
@inject
async def stream_chunk(
    view_chunk: FromDishka[ViewChunk[PNGImageChunkView, Any]],
    chunk_number_x: ChunkNumberX,
    chunk_number_y: ChunkNumberY,
) -> Response:
    result = await view_chunk(chunk_number_x, chunk_number_y)

    image_stream = result.chunk_view.to_stream()

    extention_model = RecoloredPixelListSchema.of(result.pixels)
    extention = extention_model.model_dump_json()

    headers = {"extention": extention}

    return Response(image_stream, media_type="image/png", headers=headers)
