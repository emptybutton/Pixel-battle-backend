from dataclasses import dataclass

import typenv


_env = typenv.Env()


@dataclass(kw_only=True, frozen=True, slots=True)
class Env:
    redis_cluster_url = _env.str("REDIS_CLUSTER_URL")
    jwt_secret = _env.str("JWT_SECRET")
