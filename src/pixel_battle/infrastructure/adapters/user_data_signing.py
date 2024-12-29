from dataclasses import dataclass, field
from datetime import datetime

import jwt

from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningAsIdentification(UserDataSigning[User]):
    async def signed_user_data_when(self, *, user: User) -> User:
        return user

    async def user_when(self, *, signed_user_data: User) -> User | None:
        return signed_user_data


@dataclass(kw_only=True, frozen=True, slots=True)
class UserDataSigningToHS256JWT(UserDataSigning[str]):
    secret: str = field(repr=False)

    async def signed_user_data_when(self, *, user: User) -> str:
        iso_time = str(user.time_of_obtaining_recoloring_right.datetime)
        mapping = {"iso_time_of_obtaining_recoloring_right": iso_time}

        return jwt.encode(mapping, self.secret, algorithm="HS256")

    async def user_when(self, *, signed_user_data: str) -> User | None:
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
