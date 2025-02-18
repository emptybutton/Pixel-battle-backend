from datetime import datetime

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from pixel_battle.application.interactors.view_user import ViewUser
from pixel_battle.presentation.web.cookies import UserDataCookie


view_user_router = APIRouter()


class UserDataSchema(BaseModel):
    time_of_obtaining_recoloring_right: datetime = Field(
        alias="timeOfObtainingRecoloringRight"
    )
    has_recoloring_right: bool = Field(alias="hasRecoloringRight")


class UserSchema(BaseModel):
    data: UserDataSchema | None = Field(alias="data")


@view_user_router.get(
    "/pixel-battle/user",
    description="Reading current user data in the game.",
    responses={status.HTTP_200_OK: {"model": UserSchema}},
)
@inject
async def view_user(
    view_user: FromDishka[ViewUser[str]],
    user_data: UserDataCookie.StrOrNone = None,
) -> JSONResponse:
    result = await view_user(signed_user_data=user_data)

    if result is None:
        user_data_model = None
    else:
        user_data_model = UserDataSchema(
            hasRecoloringRight=result.has_recoloring_right,
            timeOfObtainingRecoloringRight=(
                result.time_of_obtaining_recoloring_right.datetime
            ),
        )

    response_body_model = UserSchema(data=user_data_model)
    response_body = response_body_model.model_dump(by_alias=True, mode="json")

    return JSONResponse(response_body)
