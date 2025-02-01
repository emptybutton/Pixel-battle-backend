from dataclasses import dataclass

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    token: str | None


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewPixelBattleAdminKey:
    clock: Clock
    pixel_battle_container: PixelBattleContainer

    async def __call__(self) -> Output:
        pixel_battle = await self.pixel_battle_container.get()
        token = None if pixel_battle is None else pixel_battle.admin_key.token

        return Output(token=token)
