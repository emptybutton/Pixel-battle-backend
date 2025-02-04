from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Admin:
    key: "AdminKey"


@dataclass(kw_only=True, frozen=True, slots=True)
class AdminKey:
    token: str


def has_access(admin: Admin, *, key: AdminKey) -> bool:
    return admin.key == key
