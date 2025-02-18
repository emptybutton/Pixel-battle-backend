from typing import Literal

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from pixel_battle.application.interactors.register_user import RegisterUser
from pixel_battle.entities.core.user import (
    UserIsAlreadyRegisteredToRegisterError,
)
from pixel_battle.presentation.web.cookies import UserDataCookie
from pixel_battle.presentation.web.schemas import (
    ErrorListSchema,
    ErrorSchema,
    NoDataSchema,
)
from pixel_battle.presentation.web.tags import Tag


register_user_router = APIRouter()


class AlreadyRegisteredSchema(ErrorSchema):
    type: Literal["AlreadyRegistered"] = "AlreadyRegistered"


@register_user_router.post(
    "/pixel-battle/user",
    description=(
        "Registration to gain access to other actions."
        " After registration, it is not allowed to"
        " recolor pixels for one minute."
    ),
    tags=[Tag.user],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorListSchema[AlreadyRegisteredSchema]
        },
    },
)
@inject
async def register_user(
    register_user: FromDishka[RegisterUser[str]],
    user_data: UserDataCookie.StrOrNone = None,
) -> JSONResponse:
    try:
        result = await register_user(signed_user_data=user_data)

    except UserIsAlreadyRegisteredToRegisterError:
        json = AlreadyRegisteredSchema().to_list().model_dump(by_alias=True)
        return JSONResponse(json, status_code=status.HTTP_403_FORBIDDEN)

    response = JSONResponse({}, status_code=status.HTTP_201_CREATED)

    cookie = UserDataCookie(response)
    cookie.set(result.signed_user_data)

    return response
