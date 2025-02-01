from dataclasses import dataclass
from datetime import datetime

from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.core.pixel_battle import (
    InitializedPixelBattle,
    initialized_pixel_battle_when,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    pixel_battle: InitializedPixelBattle


@dataclass(kw_only=True, frozen=True, slots=True)
class InitializePixelBattle:
    pixel_battle_container: PixelBattleContainer

    async def __call__(
        self,
        pixel_battle_start_datetime: datetime,
        pixel_battle_end_datetime: datetime,
    ) -> Output:
        start_time = Time(datetime=pixel_battle_start_datetime)
        end_time = Time(datetime=pixel_battle_end_datetime)
        time_delta = TimeDelta(start_time=start_time, end_time=end_time)

        pixel_battle = await self.pixel_battle_container.get()
        initialized_pixel_battle = initialized_pixel_battle_when(
            time_delta=time_delta,
            pixel_battle=pixel_battle,
        )

        return Output(pixel_battle=initialized_pixel_battle)
