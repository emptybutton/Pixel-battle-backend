import uvicorn

from pixel_battle.deployment.chunk_streaming_service.asgi import app


def main() -> None:
    uvicorn.run(app)


if __name__ == "__main__":
    main()
