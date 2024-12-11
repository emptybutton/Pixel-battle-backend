from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from pixel_battle.entities.chunk import Chunk
from pixel_battle.entities.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class User:
    id: UUID
    time_of_obtaining_recoloring_right: Time
    chunk: Chunk


def time_of_obtaining_recoloring_right_when(*, current_time: Time) -> Time:
    return current_time.map(lambda datetime: datetime + timedelta(minutes=1))


def new_user_when(*, current_time: Time, chunk: Chunk) -> User:
    user_id = uuid4()
    time = time_of_obtaining_recoloring_right_when(current_time=current_time)

    return User(
        id=user_id, time_of_obtaining_recoloring_right=time, chunk=chunk
    )


def temporarily_without_right_to_recolor(
    user: User, *, current_time: Time
) -> User:
    time = time_of_obtaining_recoloring_right_when(current_time=current_time)

    return User(
        id=user.id, chunk=user.chunk, time_of_obtaining_recoloring_right=time
    )


def has_right_to_recolor(user: User, *, current_time: Time) -> bool:
    return user.time_of_obtaining_recoloring_right >= current_time
