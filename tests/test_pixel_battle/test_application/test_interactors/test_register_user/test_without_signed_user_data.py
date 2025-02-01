from pixel_battle.application.interactors.register_user import (
    RegisterUser,
)
from pixel_battle.entities.core.user import User


async def test_reult(
    register_user: RegisterUser[User | None], registered_user: User
) -> None:
    result = await register_user(signed_user_data=None)

    assert result.signed_user_data == registered_user
