from collections.abc import AsyncIterator
from datetime import UTC, datetime
from functools import partial

from dishka import AsyncContainer, Provider, Scope, make_async_container
from pytest import Item, fixture, mark
from pytest_asyncio import is_async_test

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
)
from pixel_battle.application.interactors.register_user import (
    RegisterUser,
)
from pixel_battle.application.interactors.view_chunk import (
    ViewChunk,
)
from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_battle_container import (
    PixelBattleContainer,
)
from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.admin.admin import AdminKey
from pixel_battle.entities.core.pixel_battle import InitiatedPixelBattle
from pixel_battle.entities.space.time import Time
from pixel_battle.entities.space.time_delta import TimeDelta
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultPNGImageChunkViewWhen,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_views import (
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.pixel_battle_container import (
    InMemoryPixelBattleContainer,
)
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.presentation.web.streaming import Streaming


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(
        lambda: Time(datetime=datetime(2006, 1, 1, tzinfo=UTC)),
        provides=Time,
    )
    provider.provide(
        lambda: UserDataSigningToHS256JWT(secret="super secret secret"),
        provides=UserDataSigning[str],
    )
    provider.provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )
    provider.provide(
        lambda: InMemoryChunkViews(), provides=ChunkViews[PNGImageChunkView]
    )
    provider.provide(lambda: InMemoryPixelQueue(), provides=PixelQueue)
    provider.provide(StoppedClock, provides=Clock)
    provider.provide(RecolorPixel[str])
    provider.provide(ViewChunk[PNGImageChunkView])
    provider.provide(ViewChunkStream)
    provider.provide(RegisterUser[str])
    provider.provide(
        RefreshChunkView[PNGImageChunkView],
        provides=RefreshChunkView[ChunkView],
    )

    @provider.provide
    def provide_pixel_battle_container() -> PixelBattleContainer:
        start_time = Time(datetime=datetime(1981, 1, 1, tzinfo=UTC))
        end_time = Time(datetime=datetime(2077, 1, 1, tzinfo=UTC))
        time_delta = TimeDelta(start_time=start_time, end_time=end_time)

        admin_key = AdminKey(token="token")
        pixel_battle = InitiatedPixelBattle(
            admin_key=admin_key, time_delta=time_delta
        )

        return InMemoryPixelBattleContainer(pixel_battle)

    @partial(provider.provide, provides=Streaming)
    async def get_streaming(
        view_chunk_stream: ViewChunkStream
    ) -> AsyncIterator[Streaming]:
        async with Streaming(view_chunk_stream=view_chunk_stream) as streaming:
            yield streaming

    return make_async_container(provider)
