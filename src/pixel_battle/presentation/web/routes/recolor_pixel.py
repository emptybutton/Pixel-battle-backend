from datetime import datetime
from typing import Literal

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import (
    PixelOutOfCanvasError,
    UserHasNoRightToRecolorError,
)
from pixel_battle.entities.quantities.color import (
    RGBColorValueNumberInInvalidRangeError,
)
from pixel_battle.presentation.web.cookies import (
    DatetimeOfObtainingRecoloringRightCookie,
)
from pixel_battle.presentation.web.schemas import ErrorListSchema, ErrorSchema


pixel_recoloring_router = APIRouter()


class RecolorPixelSchema(BaseModel):
    pixel_position: tuple[int, int] = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] = Field(alias="newPixelColor")


class InvalidColorValueRangeSchema(ErrorSchema):
    type: Literal["invalidColorValueRange"] = "invalidColorValueRange"


class PixelOutOfCanvasSchema(ErrorSchema):
    type: Literal["pixelOutOfCanvas"] = "pixelOutOfCanvas"


class NoRightSchema(ErrorSchema):
    type: Literal["noRight"] = "noRight"


@pixel_recoloring_router.patch(
    "/canvas",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorListSchema[
                InvalidColorValueRangeSchema | PixelOutOfCanvasSchema
            ]
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorListSchema[NoRightSchema]
        },
    },
)
@inject
async def recolor_pixel(
    recolor_pixel: FromDishka[RecolorPixel],
    body_model: RecolorPixelSchema,
    iso_time: DatetimeOfObtainingRecoloringRightCookie.IsoTimeOrNone = None,
) -> JSONResponse:
    datetime_ = None if iso_time is None else datetime.fromisoformat(iso_time)

    try:
        result = await recolor_pixel(
            datetime_of_obtaining_recoloring_right=datetime_,
            pixel_position_x=body_model.pixel_position[0],
            pixel_position_y=body_model.pixel_position[1],
            new_color_red_value_number=body_model.new_pixel_color[0],
            new_color_green_value_number=body_model.new_pixel_color[1],
            new_color_blue_value_number=body_model.new_pixel_color[2],
        )

    except PixelOutOfCanvasError:
        json = PixelOutOfCanvasSchema().model_dump()
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except RGBColorValueNumberInInvalidRangeError:
        json = InvalidColorValueRangeSchema().model_dump()
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except UserHasNoRightToRecolorError:
        json = NoRightSchema().model_dump()
        return JSONResponse(json, status_code=status.HTTP_403_FORBIDDEN)

    response = JSONResponse({}, status_code=status.HTTP_200_OK)

    cookie = DatetimeOfObtainingRecoloringRightCookie(response)
    cookie.set(result.user.time_of_obtaining_recoloring_right.datetime)

    return response
