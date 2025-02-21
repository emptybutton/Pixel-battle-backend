from dataclasses import dataclass

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class Envs:
    canvas_redis_cluster_url: str
    canvas_metadata_redis_cluster_url: str
    jwt_secret: str
    admin_key: str
    chunk_refreh_task_pushing_interval_seconds: int | float

    @classmethod
    def load(cls) -> "Envs":
        loader = typenv.Env()

        return Envs(
            canvas_redis_cluster_url=(
                loader.str("CANVAS_REDIS_CLUSTER_URL")
            ),
            canvas_metadata_redis_cluster_url=(
                loader.str("CANVAS_METADATA_REDIS_CLUSTER_URL")
            ),
            jwt_secret=loader.str("JWT_SECRET"),
            admin_key=loader.str("ADMIN_KEY"),
            chunk_refreh_task_pushing_interval_seconds=(
                loader.float("CHUNK_REFREH_TASK_PUSHING_INTERVAL_SECONDS")
            ),
        )
