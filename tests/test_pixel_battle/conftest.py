from pytest import Item, mark
from pytest_asyncio import is_async_test


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
