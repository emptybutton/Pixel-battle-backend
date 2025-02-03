from dataclasses import dataclass
from enum import Enum, auto

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.pixel_battle import is_initiated


@dataclass(kw_only=True, frozen=True, slots=True)
class Ok:
    admin_key: AdminKey


class Error(Enum):
    pixel_battle_is_not_initiated_error = auto()


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewPixelBattleAdminKey:
    clock: Clock
    pixel_battle_container: PixelBattleContainer

    async def __call__(self) -> Ok | Error:
        pixel_battle = await self.pixel_battle_container.get()

        if not is_initiated(pixel_battle):
            return Error.pixel_battle_is_not_initiated_error

        return Ok(admin_key=pixel_battle.admin_key)
