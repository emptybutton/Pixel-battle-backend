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
async def view_chunk(
    view_chunk: FromDishka[ViewChunk[PNGImageChunkView, Any]],
    chunk_number_x: ChunkNumberX,
    chunk_number_y: ChunkNumberY,
) -> Response:
    result = await view_chunk(chunk_number_x, chunk_number_y)

    extension_model = RecoloredPixelListSchema.of(result.pixels)
    extension = extension_model.model_dump_json(by_alias=True)

    headers = {"extension": extension}

    image_stream = result.chunk_view.to_stream()
    content = image_stream.getvalue()
    image_stream.close()

    return Response(content, media_type="image/png", headers=headers)
