from abc import ABC, abstractmethod
from uuid import UUID

from pixel_battle.entities.core.user import User


class Users(ABC):
    @abstractmethod
    async def user_with_id(self, id: UUID) -> User | None: ...

    @abstractmethod
    async def put(self, user: User) -> None: ...
