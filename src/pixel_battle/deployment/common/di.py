from collections.abc import AsyncIterator
from typing import Any

from dishka import Provider, Scope, alias, provide
from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.refresh_chunk import (
    RefreshChunk,
)
from pixel_battle.application.interactors.register_user import RegisterUser
from pixel_battle.application.interactors.schedule_pixel_battle import (
    SchedulePixelBattle,
)
from pixel_battle.application.interactors.view_chunk import (
    ViewChunk,
)
from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.application.interactors.view_pixel_battle import (
    ViewPixelBattle,
)
from pixel_battle.application.interactors.view_user import ViewUser
from pixel_battle.application.ports.chunk_optimistic_lock import (
    ChunkOptimisticLockWhen,
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
from pixel_battle.entities.core.pixel_battle import UnscheduledPixelBattle
from pixel_battle.infrastructure.adapters.chunk_optimistic_lock import (
    AsyncIOChunkOptimisticLockWhen,
    RedisClusterChunkOptimisticLockWhen,
)
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultPNGImageChunkViewWhen,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_views import (
    InMemoryChunkViews,
    InRedisClusterPNGImageChunkViews,
)
from pixel_battle.infrastructure.adapters.clock import (
    LocalClock,
    RedisClusterRandomNodeClock,
)
from pixel_battle.infrastructure.adapters.pixel_battle_container import (
    InMemoryPixelBattleContainer,
    RedisClusterPixelBattleContainer,
)
from pixel_battle.infrastructure.adapters.pixel_queue import (
    InMemoryPixelQueue,
    RedisClusterStreamPixelQueue,
)
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.infrastructure.envs import Envs
from pixel_battle.presentation.distributed_tasks.refresh_chunk import (
    RefreshChunkTask,
)
from pixel_battle.presentation.web.streaming import Streaming


type CanvasRedisCluster = RedisCluster
type CanvasMetadataRedisCluster = RedisCluster


class OutOfProcessInfrastructureProvider(Provider):
    scope = Scope.APP

    provide_envs = provide(source=Envs.load)

    @provide
    async def provide_canvas_redis_cluster(
        self, envs: Envs
    ) -> AsyncIterator[CanvasRedisCluster]:
        cluster = RedisCluster.from_url(envs.canvas_redis_cluster_url)

        async with cluster:
            yield cluster

    @provide
    async def provide_canvas_metadata_redis_cluster(
        self, envs: Envs
    ) -> AsyncIterator[CanvasMetadataRedisCluster]:
        cluster = RedisCluster.from_url(envs.canvas_metadata_redis_cluster_url)

        async with cluster:
            yield cluster


class OutOfProcessInfrastructureAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_user_data_signing(self, envs: Envs) -> UserDataSigning[str]:
        return UserDataSigningToHS256JWT(secret=envs.jwt_secret)

    @provide
    def provide_chunk_views(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> ChunkViews[PNGImageChunkView]:
        return InRedisClusterPNGImageChunkViews(
            redis_cluster=canvas_redis_cluster,
            close_when_putting=True,
        )

    @provide
    def provide_chunk_optimistic_lock_when(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> ChunkOptimisticLockWhen:
        return RedisClusterChunkOptimisticLockWhen(
            redis_cluster=canvas_redis_cluster,
            lock_max_age_seconds=60 * 5,
        )

    @provide
    def provide_pixel_queue(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> PixelQueue:
        return RedisClusterStreamPixelQueue(redis_cluster=canvas_redis_cluster)

    @provide
    def provide_clock(self, canvas_redis_cluster: CanvasRedisCluster) -> Clock:
        return RedisClusterRandomNodeClock(
            redis_cluster=canvas_redis_cluster
        )

    @provide
    def provide_pixel_battle_container(
        self,
        canvas_metadata_redis_cluster: CanvasMetadataRedisCluster,
        envs: Envs,
    ) -> PixelBattleContainer:
        return RedisClusterPixelBattleContainer(
            redis_cluster=canvas_metadata_redis_cluster,
            admin_key=AdminKey(token=envs.admin_key),
        )

    provide_default_png_image_chunk_view_when = provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )


class ProcessInfrastructureAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_user_data_signing(self) -> UserDataSigning[str]:
        return UserDataSigningToHS256JWT(secret="super secret secret")  # noqa: S106

    @provide
    def provide_pixel_battle_container(self) -> PixelBattleContainer:
        admin_key = AdminKey(token="admin-key")  # noqa: S106
        pixel_battle = UnscheduledPixelBattle(admin_key=admin_key)

        return InMemoryPixelBattleContainer(pixel_battle)

    provide_chunk_optimistic_lock_when = provide(
        AsyncIOChunkOptimisticLockWhen, provides=ChunkOptimisticLockWhen,
    )

    provide_chunk_views = provide(
        lambda _: InMemoryChunkViews(), provides=ChunkViews[PNGImageChunkView]
    )
    provide_pixel_queue = provide(
        lambda _: InMemoryPixelQueue(), provides=PixelQueue
    )
    provide_clock = provide(LocalClock, provides=Clock)

    provide_default_png_image_chunk_view_when = provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )


class InteractorProvider(Provider):
    scope = Scope.APP

    provide_register_user = provide(RegisterUser[str])
    provide_any_register_user = alias(
        source=RegisterUser[str], provides=RegisterUser[Any]
    )

    provide_recolor_pixel = provide(RecolorPixel[str])
    provide_view_chunk_stream = provide(ViewChunkStream)

    provide_schedule_pixel_battle = provide(SchedulePixelBattle)
    provide_view_pixel_battle = provide(ViewPixelBattle)

    provide_refresh_chunk = provide(RefreshChunk[PNGImageChunkView])
    provide_any_refresh_chunk = alias(
        source=RefreshChunk[PNGImageChunkView],
        provides=RefreshChunk[ChunkView],
    )

    provide_view_chunk = provide(ViewChunk[PNGImageChunkView])
    provide_any_view_chunk = alias(
        source=ViewChunk[PNGImageChunkView],
        provides=ViewChunk[ChunkView],
    )

    provide_view_user = provide(ViewUser[str])
    provide_any_view_user = alias(source=ViewUser[str], provides=ViewUser[Any])


class StreamingProvider(Provider):
    scope = Scope.APP

    @provide(provides=Streaming)
    async def provide_streaming(
        self, view_chunk_stream: ViewChunkStream
    ) -> AsyncIterator[Streaming]:
        async with Streaming(view_chunk_stream=view_chunk_stream) as streaming:
            yield streaming


class DistributedTaskProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_update_chunk_task(
        self,
        canvas_metadata_redis_cluster: CanvasMetadataRedisCluster,
        refresh_chunk: RefreshChunk[ChunkView],
    ) -> RefreshChunkTask:
        return RefreshChunkTask(
            refresh_chunk=refresh_chunk,
            redis_cluster=canvas_metadata_redis_cluster,
            pulling_interval_seconds=20,
        )
