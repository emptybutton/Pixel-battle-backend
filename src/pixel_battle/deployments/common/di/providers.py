from typing import Any, AsyncIterator, Iterable

from dishka import Provider, Scope, provide
from fastapi import APIRouter
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
from pixel_battle.application.ports.lock import Lock
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.infrastructure.adapters.broker import (
    RedisClusterStreamBroker,
)
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultPNGImageChunkViewWhen,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_views import (
    InRedisClusterPNGImageChunkViews,
)
from pixel_battle.infrastructure.adapters.clock import (
    RedisClusterRandomNodeClock,
)
from pixel_battle.infrastructure.adapters.lock import (
    InRedisClusterLock,
)
from pixel_battle.infrastructure.adapters.offsets import (
    InRedisClusterRedisStreamOffsets,
)
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.infrastructure.envs import Envs
from pixel_battle.infrastructure.redis.types import RedisStreamOffset
from pixel_battle.presentation.distributed_tasks.update_chunk_view import (
    UpdateChunkViewTask,
)
from pixel_battle.presentation.scripts.update_chunk_view import (
    UpdateChunkViewScript,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)
from pixel_battle.presentation.web.streaming import Streaming


type CanvasRedisCluster = RedisCluster
type CanvasMetadataRedisCluster = RedisCluster


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide()
    def provide_envs(self) -> Envs:
        return Envs.load

    @provide()
    async def provide_canvas_redis_cluster(
        self, envs: Envs
    ) -> AsyncIterator[CanvasRedisCluster]:
        cluster = RedisCluster.from_url(envs.canvas_redis_cluster_url)

        async with cluster:
            yield cluster

    @provide()
    async def provide_canvas_metadata_redis_cluster(
        self, envs: Envs
    ) -> AsyncIterator[CanvasMetadataRedisCluster]:
        cluster = RedisCluster.from_url(envs.canvas_metadata_redis_cluster_url)

        async with cluster:
            yield cluster


class AdapterProvider(Provider):
    scope = Scope.APP

    @provide()
    def provide_user_data_signing(self, envs: Envs) -> UserDataSigning[str]:
        return UserDataSigningToHS256JWT(secret=envs.jwt_secret)

    @provide()
    def provide_chunk_views(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> ChunkViews[PNGImageChunkView]:
        return InRedisClusterPNGImageChunkViews(
            redis_cluster=canvas_redis_cluster,
            close_when_putting=True,
        )

    @provide()
    def provide_broker(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> Broker[RedisStreamOffset] | Broker[Any]:
        return RedisClusterStreamBroker(redis_cluster=canvas_redis_cluster)

    @provide()
    def provide_lock(self, canvas_redis_cluster: CanvasRedisCluster) -> Lock:
        return InRedisClusterLock(redis_cluster=canvas_redis_cluster)

    @provide()
    def provide_offsets(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> InRedisClusterRedisStreamOffsets:
        return InRedisClusterRedisStreamOffsets(
            redis_cluster=canvas_redis_cluster
        )

    @provide()
    def provide_clock(
        self, canvas_redis_cluster: CanvasRedisCluster
    ) -> RedisClusterRandomNodeClock:
        return RedisClusterRandomNodeClock(
            redis_cluster=canvas_redis_cluster
        )

    provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )


class InteractorProvider(Provider):
    scope = Scope.APP

    provide(RecolorPixel[str])
    provide(UpdateChunkView[PNGImageChunkView, int])
    provide(
        ViewChunk[PNGImageChunkView, int],
        provides=ViewChunk[PNGImageChunkView, Any],
    )
    provide(ViewChunkStream)


class ChunkWritingServiceProvider(Provider):
    scope = Scope.APP
    provide(lambda: [recolor_pixel_router], provides=Iterable[APIRouter])


class ChunkReadingServiceProvider(Provider):
    scope = Scope.APP
    provide(lambda: [view_chunk_router], provides=Iterable[APIRouter])


class ChunkStreamingServiceProvider(Provider):
    scope = Scope.APP
    provide(lambda: [stream_chunk_router], provides=Iterable[APIRouter])


class StreamingProvider(Provider):
    scope = Scope.APP

    @provide(provides=Streaming)
    async def provide_streaming(
        self, view_chunk_stream: ViewChunkStream
    ) -> AsyncIterator[Streaming]:
        async with Streaming(view_chunk_stream=view_chunk_stream) as streaming:
            yield streaming


class GodServiceProvider(Provider):
    scope = Scope.APP

    provide(
        lambda: [recolor_pixel_router, view_chunk_router, stream_chunk_router],
        provides=Iterable[APIRouter]
    )


class ScriptProvider(Provider):
    scope = Scope.APP

    provide(UpdateChunkViewScript)


class DistributedTaskProvider(Provider):
    scope = Scope.APP

    @provide()
    def provide_update_chunk_view_task(
        self,
        canvas_metadata_redis_cluster: CanvasMetadataRedisCluster,
        update_chunk_view: UpdateChunkView[PNGImageChunkView, int],
    ) -> UpdateChunkViewTask:
        return UpdateChunkViewTask(
            update_chunk_view=update_chunk_view,
            redis_cluster=canvas_metadata_redis_cluster,
        )
