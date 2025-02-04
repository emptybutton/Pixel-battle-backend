from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.view_pixel_battle import (
    ViewPixelBattle,
)
from pixel_battle.presentation.web.schemas import (
    TimeDeltaSchema,
)


router = APIRouter()


class PixelBattleSchema(BaseModel):
    is_going_on: bool = Field(alias="isGoingOn")
    time_delta: TimeDeltaSchema | None = Field(alias="timeDelta")


@router.get(
    "/",
    description="Reading state of the game.",
    responses={status.HTTP_200_OK: {"model": PixelBattleSchema}},
)
@inject
async def view_pixel_battle(
    view_pixel_battle: FromDishka[ViewPixelBattle],
) -> JSONResponse:
    result = await view_pixel_battle()

    if result.pixel_battle_time_delta is None:
        time_delta = None
    else:
        time_delta = TimeDeltaSchema.of(result.pixel_battle_time_delta)

    reponse_body_model = PixelBattleSchema(
        isGoingOn=result.is_pixel_battle_going_on, timeDelta=time_delta
    )
    reponse_body = reponse_body_model.model_dump(by_alias=True)
    return JSONResponse(reponse_body)
