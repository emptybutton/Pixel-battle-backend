import uvicorn


def run_dev(app_path: str) -> None:
    uvicorn.run(
        app_path,
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
        reload_dirs=["/pixel-battle"],
    )
