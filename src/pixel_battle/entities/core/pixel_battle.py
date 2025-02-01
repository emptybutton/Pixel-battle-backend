from dataclasses import dataclass
from typing import TypeGuard, cast

from pixel_battle.entities.admin.admin import (
    Admin,
    AdminKey,
    generated_admin_key_when,
    has_access,
)
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta


@dataclass(kw_only=True, frozen=True, slots=True)
class InitiatedPixelBattle:
    time_delta: TimeDelta
    admin_key: AdminKey


type UninitiatedPixelBattle = None
type PixelBattle = InitiatedPixelBattle | UninitiatedPixelBattle


def is_initiated(pixel_battle: PixelBattle) -> TypeGuard[InitiatedPixelBattle]:
    return pixel_battle is not None


class PixelBattleIsAlreadyInitiatedError(Exception): ...


def initiated_pixel_battle_when(
    *, time_delta: TimeDelta, pixel_battle: PixelBattle
) -> InitiatedPixelBattle:
    if is_initiated(pixel_battle):
        raise PixelBattleIsAlreadyInitiatedError

    admin_key = generated_admin_key_when()
    return InitiatedPixelBattle(time_delta=time_delta, admin_key=admin_key)


class NoAccessToRescheduleError(Exception): ...


def rescheduled_by_admin(
    pixel_battle: PixelBattle,
    *,
    new_time_delta: TimeDelta,
    admin: Admin,
) -> InitiatedPixelBattle:
    if not has_access_to_pixel_battle(admin, pixel_battle=pixel_battle):
        raise NoAccessToRescheduleError

    pixel_battle = cast(InitiatedPixelBattle, pixel_battle)

    return InitiatedPixelBattle(
        time_delta=new_time_delta,
        admin_key=pixel_battle.admin_key,
    )


def is_going_on(pixel_battle: PixelBattle, *, current_time: Time) -> bool:
    if not is_initiated(pixel_battle):
        return False

    return current_time in pixel_battle.time_delta


def has_access_to_pixel_battle(
    admin: Admin, *, pixel_battle: PixelBattle
) -> bool:
    if not is_initiated(pixel_battle):
        return False

    return has_access(admin, key=pixel_battle.admin_key)
