
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.schedule_pixel_battle import (
    SchedulePixelBattle,
)
from pixel_battle.entities.core.pixel_battle import NotAuthorizedToScheduleError
from pixel_battle.entities.space.time import NotUTCTimeError
from pixel_battle.entities.space.time_delta import StartAfterEndTimeDeltaError
from pixel_battle.presentation.web.headers import AdminKeyHeader
from pixel_battle.presentation.web.schemas import (
    ErrorListSchema,
    NoAdminKeySchema,
    NoDataSchema,
    NoRightSchema,
    NotUTCTimeSchema,
    StartAfterEndTimeDeltaSchema,
    TimeDeltaSchema,
)
from pixel_battle.presentation.web.tags import Tag


schedule_pixel_battle_router = APIRouter()


class SchedulePixelBattleSchema(BaseModel):
    time_delta: TimeDeltaSchema = Field(alias="timeDelta")


@schedule_pixel_battle_router.patch(
    "/pixel-battle",
    description="Updating state of the game. Requires admin key.",
    tags=[Tag.configuration],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": NoDataSchema},
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorListSchema[NoRightSchema]
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": (
                ErrorListSchema[NoAdminKeySchema]
                | ErrorListSchema[NotUTCTimeSchema]
                | ErrorListSchema[StartAfterEndTimeDeltaSchema]
            )
        },
    },
)
@inject
async def schedule_pixel_battle(
    schedule_pixel_battle: FromDishka[SchedulePixelBattle],
    admin_key: AdminKeyHeader.CredentialsOrNone,
    body_model: SchedulePixelBattleSchema,
) -> JSONResponse:
    if admin_key is None:
        json = NoAdminKeySchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    try:
        timedelta = body_model.time_delta
        await schedule_pixel_battle(
            admin_key_token=admin_key.credentials,
            pixel_battle_start_datetime=timedelta.start_time,
            pixel_battle_end_datetime=timedelta.end_time,
        )

    except NotUTCTimeError:
        json = NotUTCTimeSchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except StartAfterEndTimeDeltaError:
        json = (
            StartAfterEndTimeDeltaSchema().to_list().model_dump(by_alias=True)
        )
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except NotAuthorizedToScheduleError:
        json = NoRightSchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_403_FORBIDDEN)

    return JSONResponse({}, status_code=status.HTTP_200_OK)
