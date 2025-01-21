from dataclasses import dataclass
from datetime import timedelta
from typing import Annotated, ClassVar

from fastapi import Cookie, Depends, Response
from fastapi.security import APIKeyCookie


@dataclass(frozen=True, slots=True)
class UserDataCookie:
    __name: ClassVar = "userData"
    __api_key: ClassVar = APIKeyCookie(
        name=__name,
        scheme_name="User data cookie",
        description=(
            "Required for various actions. Obtained after registration."
        ),
    )

    StrOrNone: ClassVar = Annotated[str | None, Cookie(alias=__name)]
    Str: ClassVar = Annotated[str, Depends(__api_key)]

    response: Response

    def set(self, user_data: str) -> None:
        self.response.set_cookie(
            self.__name,
            user_data,
            httponly=True,
            max_age=int(timedelta(days=365 * 5).total_seconds()),
        )
