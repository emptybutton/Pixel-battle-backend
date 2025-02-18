from pixel_battle.deployment.common.uvicorn import run_dev


def main() -> None:
    run_dev("pixel_battle.deployment.showcase_service.asgi:app")


if __name__ == "__main__":
    main()
