from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.entities.core.pixel import (
    PixelOutOfCanvasError,
    UserHasNoRightToRecolorError,
)
from pixel_battle.entities.space.color import (
    RGBColorValueNumberInInvalidRangeError,
)
from pixel_battle.presentation.web.cookies import UserDataCookie
from pixel_battle.presentation.web.schemas import (
    ErrorListSchema,
    InvalidColorValueRangeSchema,
    NoDataSchema,
    NoRightSchema,
    PixelOutOfCanvasSchema,
)
from pixel_battle.presentation.web.tags import Tag


recolor_pixel_router = APIRouter()


class RecolorPixelSchema(BaseModel):
    pixel_position: tuple[int, int] = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] = Field(alias="newPixelColor")


@recolor_pixel_router.patch(
    "/pixel-battle/canvas",
    description=(
        "Recoloring one pixel on the canvas."
        " After recoloring, the action will be unavailable for one minute."
    ),
    tags=[Tag.canvas],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": NoDataSchema
        },
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
    recolor_pixel: FromDishka[RecolorPixel[str]],
    body_model: RecolorPixelSchema,
    user_data: UserDataCookie.Str,
) -> JSONResponse:
    try:
        result = await recolor_pixel(
            signed_user_data=user_data,
            pixel_position_x=body_model.pixel_position[0],
            pixel_position_y=body_model.pixel_position[1],
            new_color_red_value_number=body_model.new_pixel_color[0],
            new_color_green_value_number=body_model.new_pixel_color[1],
            new_color_blue_value_number=body_model.new_pixel_color[2],
        )

    except RGBColorValueNumberInInvalidRangeError:
        json = InvalidColorValueRangeSchema().to_list().model_dump(
            by_alias=True
        )
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except PixelOutOfCanvasError:
        json = PixelOutOfCanvasSchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_400_BAD_REQUEST)

    except UserHasNoRightToRecolorError:
        json = NoRightSchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_403_FORBIDDEN)

    response = JSONResponse({}, status_code=status.HTTP_200_OK)

    cookie = UserDataCookie(response)
    cookie.set(result.signed_user_data)

    return response
