from dataclasses import dataclass
from datetime import datetime

from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.admin.admin import Admin, AdminKey
from pixel_battle.entities.core.pixel_battle import (
    InitializedPixelBattle,
    rescheduled_by_admin,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    pixel_battle: InitializedPixelBattle


@dataclass(kw_only=True, frozen=True, slots=True)
class ReshedulePixelBattle:
    pixel_battle_container: PixelBattleContainer

    async def __call__(
        self,
        pixel_battle_start_datetime: datetime,
        pixel_battle_end_datetime: datetime,
        admin_key_token: str,
    ) -> Output:
        admin_key = AdminKey(token=admin_key_token)
        admin = Admin(key=admin_key)

        start_time = Time(datetime=pixel_battle_start_datetime)
        end_time = Time(datetime=pixel_battle_end_datetime)
        new_time_delta = TimeDelta(start_time=start_time, end_time=end_time)

        stored_pixel_battle = await self.pixel_battle_container.get()

        rescheduled_pixel_battle = rescheduled_by_admin(
            stored_pixel_battle,
            new_time_delta=new_time_delta,
            admin=admin,
        )

        return Output(pixel_battle=rescheduled_pixel_battle)
