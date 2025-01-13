from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response


router = APIRouter()


@router.get("/healthchek")
def healthchek() -> Response:
    return JSONResponse({})
