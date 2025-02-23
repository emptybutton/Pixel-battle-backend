from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket

from pixel_battle.presentation.web.params import ChunkNumberX, ChunkNumberY
from pixel_battle.presentation.web.streaming import Streaming, StreamingClient


stream_chunk_router = APIRouter()


@stream_chunk_router.websocket(
    "/pixel-battle/canvas/chunk/{chunk_number_x}/{chunk_number_y}/stream"
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

    client = StreamingClient(websocket=websocket, group_id=group_id)
    streaming.add_client(client)
