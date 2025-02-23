from dataclasses import dataclass

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.user import has_recoloring_right
from pixel_battle.entities.space.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class OutputData:
    time_of_obtaining_recoloring_right: Time
    has_recoloring_right: bool


type Output = OutputData | None


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewUser[SignedUserDataT]:
    user_data_signing: UserDataSigning[SignedUserDataT]
    clock: Clock

    async def __call__(
        self, signed_user_data: SignedUserDataT | None
    ) -> Output:
        if signed_user_data is None:
            return None

        current_time = await self.clock.get_current_time()

        user = (
            await self.user_data_signing
            .user_when(signed_user_data=signed_user_data)
        )

        if user is None:
            return None

        return OutputData(
            time_of_obtaining_recoloring_right=(
                user.time_of_obtaining_recoloring_right
            ),
            has_recoloring_right=(
                has_recoloring_right(user, current_time=current_time)
            ),
        )
