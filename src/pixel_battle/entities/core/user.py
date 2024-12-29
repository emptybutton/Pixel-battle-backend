from dataclasses import dataclass
from datetime import timedelta

from pixel_battle.entities.space.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class User:
    time_of_obtaining_recoloring_right: Time


def time_of_obtaining_recoloring_right_when(*, current_time: Time) -> Time:
    return current_time.map(lambda datetime: datetime + timedelta(minutes=1))


def user_temporarily_without_recoloring_right_when(
    *, current_time: Time
) -> User:
    time = time_of_obtaining_recoloring_right_when(current_time=current_time)

    return User(time_of_obtaining_recoloring_right=time)


def has_recoloring_right(user: User, *, current_time: Time) -> bool:
    return user.time_of_obtaining_recoloring_right <= current_time
