from pytest import fixture

from pixel_battle.entities.admin.admin import (
    Admin,
    AdminKey,
    has_access,
)


@fixture
def key1() -> AdminKey:
    return AdminKey(token="1")


@fixture
def key2() -> AdminKey:
    return AdminKey(token="2")


@fixture
def admin(key1: AdminKey) -> Admin:
    return Admin(key=key1)


def test_has_access_true(admin: Admin, key1: AdminKey) -> None:
    assert has_access(admin, key=key1)


def test_has_access_false(admin: Admin, key2: AdminKey) -> None:
    assert not has_access(admin, key=key2)
