from typing import AsyncIterator

from pytest import Item, fixture, mark
from pytest_asyncio import is_async_test
from redis.asyncio.cluster import RedisCluster

from pixel_battle.infrastructure.env import Env


@fixture(scope="session")
async def redis_cluster() -> AsyncIterator[RedisCluster]:
    async with RedisCluster.from_url(Env.redis_cluster_url) as redis_cluster:
        yield redis_cluster


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
