from collections.abc import Iterator

from fastapi import APIRouter

from pixel_battle.presentation.web.routes.healthcheck import (
    healthcheck_router,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.register_user import (
    register_user_router,
)
from pixel_battle.presentation.web.routes.schedule_pixel_battle import (
    schedule_pixel_battle_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    view_chunk_router,
)
from pixel_battle.presentation.web.routes.view_pixel_battle import (
    view_pixel_battle_router,
)
from pixel_battle.presentation.web.routes.view_user import (
    view_user_router,
)


all_routers = (
    healthcheck_router,
    view_pixel_battle_router,
    schedule_pixel_battle_router,
    view_user_router,
    register_user_router,
    recolor_pixel_router,
    view_chunk_router,
    stream_chunk_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
