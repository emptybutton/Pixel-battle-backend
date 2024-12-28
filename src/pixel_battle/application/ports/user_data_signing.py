from abc import ABC, abstractmethod

from pixel_battle.entities.core.user import User


class UserDataSigning[SignedUserDataT](ABC):
    @abstractmethod
    async def signed_user_data_when(self, *, user: User) -> SignedUserDataT: ...

    @abstractmethod
    async def user_when(
        self, *, signed_user_data: SignedUserDataT
    ) -> User | None: ...
