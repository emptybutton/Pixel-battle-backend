from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket

from pixel_battle.presentation.chunk_streaming.streaming import Streaming


router = APIRouter()


@router.websocket("/canvas/chunk/{chunk_number_x}/{chunk_number_y}")
@inject
async def chunk_streaming(
    websocket: WebSocket,
    streaming: FromDishka[Streaming],
    chunk_number_x: int,
    chunk_number_y: int,
) -> None:
    await websocket.accept()

    group_id = (chunk_number_x, chunk_number_y)
    streaming.add_client(websocket=websocket, group_id=group_id)
