from pytest import fixture

from pixel_battle.entities.core.user import User
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)


@fixture
def signing() -> UserDataSigningAsIdentification:
    return UserDataSigningAsIdentification()


async def test_isomorphism(
    signing: UserDataSigningAsIdentification, user: User
) -> None:
    signed_user_data = await signing.signed_user_data_when(user=user)
    result_user = await signing.user_when(signed_user_data=signed_user_data)

    assert user == result_user
