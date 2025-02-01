from dataclasses import dataclass
from secrets import token_hex


@dataclass(kw_only=True, frozen=True, slots=True)
class Admin:
    key: "AdminKey"


@dataclass(kw_only=True, frozen=True, slots=True)
class AdminKey:
    token: str


def generated_admin_key_when() -> AdminKey:
    return AdminKey(token=token_hex(64))


def has_access(admin: Admin, *, key: AdminKey) -> bool:
    return admin.key == key
