from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from pixel_battle.presentation.web.schemas import NoDataSchema
from pixel_battle.presentation.web.tags import Tag


healthcheck_router = APIRouter()


@healthcheck_router.get(
    "/healthcheck",
    responses={status.HTTP_200_OK: {"model": NoDataSchema}},
    description="Checking if the server can accept requests.",
    tags=[Tag.monitoring],
)
def healthcheck() -> Response:
    return JSONResponse({})
