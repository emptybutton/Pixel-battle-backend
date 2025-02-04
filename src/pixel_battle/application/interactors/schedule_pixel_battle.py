from dataclasses import dataclass
from datetime import datetime

from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.entities.admin.admin import Admin, AdminKey
from pixel_battle.entities.core.pixel_battle import (
    ScheduledPixelBattle,
    scheduled_by_admin,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    pixel_battle: ScheduledPixelBattle


@dataclass(kw_only=True, frozen=True, slots=True)
class SchedulePixelBattle:
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
        time_delta = TimeDelta(start_time=start_time, end_time=end_time)

        stored_pixel_battle = await self.pixel_battle_container.get()
        scheduled_pixel_battle = scheduled_by_admin(
            stored_pixel_battle,
            time_delta=time_delta,
            admin=admin,
        )
        await self.pixel_battle_container.put(scheduled_pixel_battle)

        return Output(pixel_battle=scheduled_pixel_battle)
