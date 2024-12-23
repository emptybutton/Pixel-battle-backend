from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, WebSocket

from pixel_battle.presentation.chunk_streaming.streaming import Streaming


router = APIRouter()


@router.websocket("/canvas/chunk/{chunk_number_x}/{chunk_number_y}")
@inject
async def chunk_streaming(
    websocket: WebSocket,
    streaming: FromDishka[Streaming],
    chunk_number_x: Annotated[
        int, Query(alias="chunkNumberX", min_length=0, max_length=9)
    ],
    chunk_number_y: Annotated[
        int, Query(alias="chunkNumberY", min_length=0, max_length=9)
    ],
) -> None:
    await websocket.accept()

    group_id = (chunk_number_x, chunk_number_y)
    streaming.add_client(websocket=websocket, group_id=group_id)
