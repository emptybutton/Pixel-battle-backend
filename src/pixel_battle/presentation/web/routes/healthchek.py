from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel


router = APIRouter()


@router.get(
    "/healthchek",
    responses={status.HTTP_200_OK: {"model": BaseModel}},
    description="Checking if the server can accept requests.",
)
def healthchek() -> Response:
    return JSONResponse({})
