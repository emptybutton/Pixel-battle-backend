from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response

from pixel_battle.application.interactors.view_chunk import ViewChunk
from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.schemas import RecoloredPixelListSchema
from pixel_battle.presentation.web.tags import Tag


view_chunk_router = APIRouter()


class ChunkViewResponse(Response):
    media_type = "image/png"


@view_chunk_router.get(
    "/pixel-battle/canvas/chunk/{chunk_number_x}/{chunk_number_y}",
    description=(
        "Reading a slightly outdated chunk image (maximum 2-5 seconds) along"
        " with the delta of changes that bring it up to date."
    ),
    tags=[Tag.canvas],
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
                    "schema": {
                        "$ref": "#/components/schemas/RecoloredPixelListSchema"
                    }
                },
            },
        },
    },
)
@inject
async def view_chunk(
    view_chunk: FromDishka[ViewChunk[ChunkView, bytes]],
    chunk_number_x: ChunkNumberX,
    chunk_number_y: ChunkNumberY,
) -> ChunkViewResponse:
    result = await view_chunk(chunk_number_x, chunk_number_y)

    actualizing_delta_model = RecoloredPixelListSchema.of(result.pixels)
    actualizing_delta = actualizing_delta_model.model_dump_json(by_alias=True)

    headers = {"X-Actualizing-Delta": actualizing_delta}

    return ChunkViewResponse(result.frozen_chunk_view, headers=headers)
