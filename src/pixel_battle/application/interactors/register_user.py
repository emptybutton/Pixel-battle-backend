from dataclasses import dataclass

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.user import registered_user_when


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[SignedUserDataT]:
    signed_user_data: SignedUserDataT


@dataclass(kw_only=True, frozen=True, slots=True)
class RegisterUser[SignedUserDataT]:
    user_data_signing: UserDataSigning[SignedUserDataT]
    clock: Clock

    async def __call__(
        self, signed_user_data: SignedUserDataT | None
    ) -> Output[SignedUserDataT]:
        current_time = await self.clock.get_current_time()

        if signed_user_data is None:
            user = None
        else:
            user = (
                await self.user_data_signing
                .user_when(signed_user_data=signed_user_data)
            )

        registered_user = registered_user_when(
            user=user, current_time=current_time
        )

        signed_user_data = (
            await self.user_data_signing
            .signed_user_data_when(user=registered_user)
        )

        return Output(signed_user_data=signed_user_data)
