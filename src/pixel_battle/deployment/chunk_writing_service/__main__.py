import uvicorn

from pixel_battle.deployment.chunk_writing_service.asgi import app


def main() -> None:
    uvicorn.run(app)


if __name__ == "__main__":
    main()
