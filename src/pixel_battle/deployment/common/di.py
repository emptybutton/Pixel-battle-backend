from typing import Any, AsyncIterator

from dishka import Provider, Scope, provide
from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.update_chunk_view import (
    UpdateChunkView,
)
from pixel_battle.application.interactors.view_chunk import (
    ViewChunk,
)
from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.application.ports.broker import Broker
from pixel_battle.application.ports.chunk_view import DefaultChunkViewWhen
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.lock import Lock
from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.infrastructure.adapters.broker import (
    InMemoryBroker,
    RedisClusterStreamBroker,
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
from pixel_battle.infrastructure.adapters.lock import (
    FakeLock,
    InRedisClusterLock,
)
from pixel_battle.infrastructure.adapters.offsets import (
    InMemoryOffsets,
    InRedisClusterRedisStreamOffsets,
)
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.infrastructure.envs import Envs
from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewTask,
)
from pixel_battle.presentation.scripts.update_chunk_view import (
    UpdateChunkViewScript,
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
    def provide_broker(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> Broker[Any]:
        return RedisClusterStreamBroker(redis_cluster=canvas_redis_cluster)

    @provide
    def provide_lock(self, canvas_redis_cluster: CanvasRedisCluster) -> Lock:
        return InRedisClusterLock(redis_cluster=canvas_redis_cluster)

    @provide
    def provide_offsets(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> Offsets[Any]:
        return InRedisClusterRedisStreamOffsets(
            redis_cluster=canvas_redis_cluster
        )

    @provide
    def provide_clock(self, canvas_redis_cluster: CanvasRedisCluster) -> Clock:
        return RedisClusterRandomNodeClock(
            redis_cluster=canvas_redis_cluster
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

    provide_chunk_views = provide(
        lambda _: InMemoryChunkViews(), provides=ChunkViews[PNGImageChunkView]
    )
    provide_broker = provide(
        lambda _: InMemoryBroker(), provides=Broker[Any]
    )
    provide_offsets = provide(lambda _: InMemoryOffsets, provides=Offsets[Any])
    provide_lock = provide(FakeLock, provides=Lock)
    provide_clock = provide(LocalClock, provides=Clock)

    provide_default_png_image_chunk_view_when = provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )


class InteractorProvider(Provider):
    scope = Scope.APP

    provide_recolor_pixel = provide(RecolorPixel[str])
    provide_update_chunk_view = provide(UpdateChunkView[PNGImageChunkView, Any])
    provide_view_chunk = provide(ViewChunk[PNGImageChunkView, Any])
    provide_view_chunk_stream = provide(ViewChunkStream)


class StreamingProvider(Provider):
    scope = Scope.APP

    @provide(provides=Streaming)
    async def provide_streaming(
        self, view_chunk_stream: ViewChunkStream
    ) -> AsyncIterator[Streaming]:
        async with Streaming(view_chunk_stream=view_chunk_stream) as streaming:
            yield streaming


class ScriptProvider(Provider):
    scope = Scope.APP

    provide_update_chunk_view_script = provide(UpdateChunkViewScript)


class DistributedTaskProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_update_chunk_view_task(
        self,
        canvas_metadata_redis_cluster: CanvasMetadataRedisCluster,
        update_chunk_view: UpdateChunkView[PNGImageChunkView, Any],
    ) -> UpdateChunkViewTask:
        return UpdateChunkViewTask(
            update_chunk_view=update_chunk_view,
            redis_cluster=canvas_metadata_redis_cluster,
        )
