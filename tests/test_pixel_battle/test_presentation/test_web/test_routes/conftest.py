from datetime import UTC, datetime

from dishka import AsyncContainer
from httpx import Cookies
from pytest import fixture

from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.core.user import User
from pixel_battle.entities.space.time import Time


@fixture
async def cookies_with_right(container: AsyncContainer) -> Cookies:
    async with container() as request_conteiner:
        signing = await request_conteiner.get(UserDataSigning[str])
        time = Time(datetime=datetime(2000, 1, 1, tzinfo=UTC))
        user = User(time_of_obtaining_recoloring_right=time)

        return Cookies({
            "userData": await signing.signed_user_data_when(user=user)
        })


@fixture
async def cookies_without_right(container: AsyncContainer) -> Cookies:
    async with container() as request_conteiner:
        signing = await request_conteiner.get(UserDataSigning[str])
        time = Time(datetime=datetime(2007, 1, 1, tzinfo=UTC))
        user = User(time_of_obtaining_recoloring_right=time)

        return Cookies({
            "userData": await signing.signed_user_data_when(user=user)
        })
