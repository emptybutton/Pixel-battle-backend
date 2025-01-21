from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response

from pixel_battle.application.interactors.view_chunk import ViewChunk
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema


router = APIRouter()


class ChunkViewResponse(Response):
    media_type = "image/png"


@router.get(
    "/canvas/chunk/{chunk_number_x}/{chunk_number_y}",
    response_class=Response,
    responses={
        status.HTTP_200_OK: {
            "content": {
                ChunkViewResponse.media_type: {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    },
                },
            },
            "headers": {
                "extension": {
                    **RecoloredPixelListSchema.model_json_schema(by_alias=True),
                },
            },
        },
    },
)
@inject
async def view_chunk(
    view_chunk: FromDishka[ViewChunk[PNGImageChunkView]],
    chunk_number_x: ChunkNumberX,
    chunk_number_y: ChunkNumberY,
) -> ChunkViewResponse:
    result = await view_chunk(chunk_number_x, chunk_number_y)

    extension_model = RecoloredPixelListSchema.of(result.pixels)
    extension = extension_model.model_dump_json(by_alias=True)

    headers = {"extension": extension}

    image_stream = result.chunk_view.to_stream()
    content = image_stream.getvalue()
    image_stream.close()

    return ChunkViewResponse(content, headers=headers)
