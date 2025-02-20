from dataclasses import dataclass, field
from datetime import datetime

import jwt

from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time
from pixel_battle.infrastructure.types import JWT


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningAsIdentification(UserDataSigning[User | None]):
    async def signed_user_data_when(self, *, user: User) -> User | None:
        return user

    async def user_when(self, *, signed_user_data: User | None) -> User | None:
        return signed_user_data


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningToHS256JWT(UserDataSigning[JWT]):
    secret: str = field(repr=False)

    async def signed_user_data_when(self, *, user: User) -> JWT:
        iso_time = str(user.time_of_obtaining_recoloring_right.datetime)
        mapping = {"iso_time_of_obtaining_recoloring_right": iso_time}

        return jwt.encode(mapping, self.secret, algorithm="HS256")

    async def user_when(self, *, signed_user_data: JWT) -> User | None:
        token = signed_user_data

        try:
            user_data = jwt.decode(token, self.secret, algorithms="HS256")
        except jwt.DecodeError:
            return None

        iso_time = user_data.get("iso_time_of_obtaining_recoloring_right")

        if iso_time is None:
            return None

        try:
            datetime_ = datetime.fromisoformat(iso_time)
        except ValueError:
            return None

        return User(time_of_obtaining_recoloring_right=Time(datetime=datetime_))
