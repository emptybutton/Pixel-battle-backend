from dataclasses import dataclass
from typing import TypeGuard

from pixel_battle.entities.admin.admin import (
    Admin,
    AdminKey,
    has_access,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class ScheduledPixelBattle:
    admin_key: AdminKey
    time_delta: TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class UnscheduledPixelBattle:
    admin_key: AdminKey


type PixelBattle = ScheduledPixelBattle | UnscheduledPixelBattle


def is_scheduled(pixel_battle: PixelBattle) -> TypeGuard[ScheduledPixelBattle]:
    return isinstance(pixel_battle, ScheduledPixelBattle)


class NotAuthorizedToScheduleError(Exception): ...


def scheduled_by_admin(
    pixel_battle: PixelBattle,
    *,
    time_delta: TimeDelta,
    admin: Admin,
) -> ScheduledPixelBattle:
    if not is_authorized(admin, pixel_battle=pixel_battle):
        raise NotAuthorizedToScheduleError

    return ScheduledPixelBattle(
        time_delta=time_delta,
        admin_key=pixel_battle.admin_key,
    )


def is_going_on(pixel_battle: PixelBattle, *, current_time: Time) -> bool:
    return (
        is_scheduled(pixel_battle) and current_time in pixel_battle.time_delta
    )


def is_authorized(
    admin: Admin, *, pixel_battle: PixelBattle
) -> bool:
    return has_access(admin, key=pixel_battle.admin_key)
