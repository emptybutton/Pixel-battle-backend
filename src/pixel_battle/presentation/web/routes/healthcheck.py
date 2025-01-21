from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel


router = APIRouter()


@router.get(
    "/healthcheck",
    responses={status.HTTP_200_OK: {"model": BaseModel}},
    description="Checking if the server can accept requests.",
)
def healthcheck() -> Response:
    return JSONResponse({})
