from dataclasses import dataclass

from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.core.pixel_battle import is_going_on
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    time_delta: TimeDelta | None
    is_pixel_battle_going_on: bool


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewPixelBattleTimeDelta:
    clock: Clock
    pixel_battle_container: PixelBattleContainer

    async def __call__(self) -> Output:
        pixel_battle = await self.pixel_battle_container.get()
        current_time = await self.clock.get_current_time()

        time_delta = None if pixel_battle is None else pixel_battle.time_delta
        is_pixel_battle_going_on = is_going_on(
            pixel_battle, current_time=current_time
        )

        return Output(
            time_delta=time_delta,
            is_pixel_battle_going_on=is_pixel_battle_going_on,
        )
