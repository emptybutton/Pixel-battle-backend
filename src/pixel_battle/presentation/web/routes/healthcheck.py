from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from pixel_battle.presentation.web.schemas import NoDataSchema


router = APIRouter()


@router.get(
    "/healthcheck",
    responses={status.HTTP_200_OK: {"model": NoDataSchema}},
    description="Checking if the server can accept requests.",
)
def healthcheck() -> Response:
    return JSONResponse({})
