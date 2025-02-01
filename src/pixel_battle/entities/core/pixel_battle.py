from dataclasses import dataclass
from typing import TypeGuard, cast

from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta
from pixel_battle.entities.admin.admin import (
    Admin, AdminKey, generated_admin_key_when, has_access
)


@dataclass(kw_only=True, frozen=True, slots=True)
class InitializedPixelBattle:
    time_delta: TimeDelta
    admin_key: AdminKey


type NotInitializedPixelBattle = None
type PixelBattle = InitializedPixelBattle | NotInitializedPixelBattle


def is_initialized(
    pixel_battle: PixelBattle
) -> TypeGuard[InitializedPixelBattle]:
    return pixel_battle is not None


class PixelBattleIsAlreadyInitializedError(Exception): ...


def initialized_pixel_battle_when(
    *, time_delta: TimeDelta, pixel_battle: PixelBattle
) -> InitializedPixelBattle:
    if is_initialized(pixel_battle):
        raise PixelBattleIsAlreadyInitializedError

    admin_key = generated_admin_key_when()
    return InitializedPixelBattle(time_delta=time_delta, admin_key=admin_key)


class NoAccessToRescheduleError(Exception): ...


def rescheduled_by_admin(
    pixel_battle: PixelBattle,
    *,
    new_time_delta: TimeDelta,
    admin: Admin,
) -> InitializedPixelBattle:
    if not has_access_to_pixel_battle(admin, pixel_battle=pixel_battle):
        raise NoAccessToRescheduleError

    pixel_battle = cast(InitializedPixelBattle, pixel_battle)

    return InitializedPixelBattle(
        time_delta=new_time_delta,
        admin_key=pixel_battle.admin_key,
    )


def is_going_on(pixel_battle: PixelBattle, *, current_time: Time) -> bool:
    if not is_initialized(pixel_battle):
        return False

    return current_time in pixel_battle.time_delta


def has_access_to_pixel_battle(
    admin: Admin, *, pixel_battle: PixelBattle
) -> bool:
    if not is_initialized(pixel_battle):
        return False

    return has_access(admin, key=pixel_battle.admin_key)
