from dataclasses import dataclass
from datetime import timedelta
from typing import Annotated, ClassVar

from fastapi import Cookie, Depends, Response


@dataclass(frozen=True, slots=True)
class UserDataCookie:
    __name: ClassVar = "userData"
    StrOrNone: ClassVar = Annotated[str | None, Depends(Cookie(alias=__name))]

    response: Response

    def set(self, user_data: str) -> None:
        self.response.set_cookie(
            self.__name,
            user_data,
            httponly=True,
            max_age=int(timedelta(days=365 * 5).total_seconds()),
        )
