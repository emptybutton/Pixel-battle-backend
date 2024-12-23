from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, ClassVar

from fastapi import Cookie, Depends, Response


@dataclass(frozen=True, slots=True)
class DatetimeOfObtainingRecoloringRightCookie:
    __name: ClassVar = "timeOfObtainingRecoloringRight"
    IsoTimeOrNone: ClassVar = Annotated[str | None, Depends(Cookie())]

    response: Response

    def set(self, time: datetime) -> None:
        self.response.set_cookie(
            self.__name,
            str(time),
            httponly=True,
            max_age=int(timedelta(days=365 * 5).total_seconds()),
        )
