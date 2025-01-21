from pixel_battle.deployment.common.uvicorn import run


def main() -> None:
    run("pixel_battle.deployment.chunk_streaming_service.asgi:app")


if __name__ == "__main__":
    main()
