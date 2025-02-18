from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response

from pixel_battle.application.interactors.view_chunk import ViewChunk
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema


view_chunk_router = APIRouter()


class ChunkViewResponse(Response):
    media_type = "image/png"


@view_chunk_router.get(
    "/pixel-battle/canvas/chunk/{chunk_number_x}/{chunk_number_y}",
    description=(
        "Reading a slightly outdated chunk image (maximum 2-5 seconds) along"
        " with the delta of changes that bring it up to date."
    ),
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
                "X-Actualizing-Delta": {
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

    actualizing_delta_model = RecoloredPixelListSchema.of(result.pixels)
    actualizing_delta = actualizing_delta_model.model_dump_json(by_alias=True)

    headers = {"X-Actualizing-Delta": actualizing_delta}

    image_stream = result.chunk_view.to_stream()
    content = image_stream.getvalue()
    image_stream.close()

    return ChunkViewResponse(content, headers=headers)
