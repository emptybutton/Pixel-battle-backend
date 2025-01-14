from typing import AsyncIterator

from dishka import Provider, Scope, alias, provide
from redis.asyncio import RedisCluster

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.refresh_chunk_view import (
    RefreshChunkView,
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
from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.application.ports.user_data_signing import UserDataSigning
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
from pixel_battle.infrastructure.adapters.pixel_queue import (
    InMemoryPixelQueue,
    RedisClusterStreamPixelQueue,
)
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.infrastructure.envs import Envs
from pixel_battle.presentation.distributed_tasks.refresh_chunk_view import (
    RefreshChunkViewTask,
)
from pixel_battle.presentation.scripts.refresh_chunk_image import (
    RefreshChunkImageScript,
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
    def provide_pixel_queue(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> PixelQueue:
        return RedisClusterStreamPixelQueue(redis_cluster=canvas_redis_cluster)

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

    provide_recolor_pixel = provide(RecolorPixel[str])
    provide_view_chunk_stream = provide(ViewChunkStream)

    provide_refresh_chunk_view = provide(RefreshChunkView[PNGImageChunkView])
    provide_any_refresh_chunk_view = alias(
        source=RefreshChunkView[PNGImageChunkView],
        provides=RefreshChunkView[ChunkView],
    )

    provide_view_chunk = provide(ViewChunk[PNGImageChunkView])
    provide_any_view_chunk = alias(
        source=ViewChunk[PNGImageChunkView],
        provides=ViewChunk[ChunkView],
    )


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

    @provide
    def provide_update_chunk_view_script(
        self, refresh_chunk_view: RefreshChunkView[PNGImageChunkView],
    ) -> RefreshChunkImageScript:
        return RefreshChunkImageScript(refresh_chunk_view=refresh_chunk_view)


class DistributedTaskProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_update_chunk_view_task(
        self,
        canvas_metadata_redis_cluster: CanvasMetadataRedisCluster,
        refresh_chunk_view: RefreshChunkView[ChunkView],
    ) -> RefreshChunkViewTask:
        return RefreshChunkViewTask(
            refresh_chunk_view=refresh_chunk_view,
            redis_cluster=canvas_metadata_redis_cluster,
        )
