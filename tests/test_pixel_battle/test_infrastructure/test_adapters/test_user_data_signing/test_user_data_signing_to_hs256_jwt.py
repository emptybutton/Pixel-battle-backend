from pytest import fixture

from pixel_battle.entities.core.user import User
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)


@fixture
def signing() -> UserDataSigningToHS256JWT:
    return UserDataSigningToHS256JWT(secret="super secret secret")


async def test_isomorphism(
    signing: UserDataSigningToHS256JWT, user: User
) -> None:
    signed_user_data = await signing.signed_user_data_when(user=user)
    result_user = await signing.user_when(signed_user_data=signed_user_data)

    assert user == result_user


async def test_user_when_with_trash(signing: UserDataSigningToHS256JWT) -> None:
    result_user = await signing.user_when(signed_user_data="trash")

    assert result_user is None
