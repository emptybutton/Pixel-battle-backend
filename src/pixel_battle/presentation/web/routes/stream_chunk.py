from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket

from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.streaming import Streaming


chunk_streaming_router = APIRouter()


@chunk_streaming_router.websocket(
    "/canvas/chunk/{chunk_number_x}/{chunk_number_y}"
)
@inject
async def stream_chunk(
    websocket: WebSocket,
    streaming: FromDishka[Streaming],
    chunk_number_x: ChunkNumberX,
    chunk_number_y: ChunkNumberY,
) -> None:
    await websocket.accept()

    group_id = (chunk_number_x, chunk_number_y)
    streaming.add_client(websocket=websocket, group_id=group_id)