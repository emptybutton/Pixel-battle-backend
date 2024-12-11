from dataclasses import dataclass
from datetime import UTC
from datetime import datetime as datetime_
from typing import Callable


class TimeError(Exception): ...


class NotUTCTimeError(TimeError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Time:
    datetime: datetime_

    def __post_init__(self) -> None:
        if self.datetime.tzinfo != UTC:
            raise NotUTCTimeError

    def map(self, mapped: Callable[[datetime_], datetime_]) -> "Time":
        return Time(datetime=mapped(self.datetime))

    def __gt__(self, other: "Time") -> bool:
        return self.datetime > other.datetime

    def __ge__(self, other: "Time") -> bool:
        return self.datetime >= other.datetime
