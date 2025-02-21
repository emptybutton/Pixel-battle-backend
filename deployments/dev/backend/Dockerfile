FROM ghcr.io/astral-sh/uv:python3.13-alpine AS pixel-battle

WORKDIR /pixel-battle
COPY . .

ENV UV_PROJECT_ENVIRONMENT /run/pixel-battle/.venv
ENV UV_CACHE_DIR /run/pixel-battle/.uv_cache

RUN uv sync

ENV PYTHONPATH /pixel-battle/src:/pixel-battle/tests
ENV MYPYPATH /pixel-battle/src:/pixel-battle/tests

ENV WATCHFILES_FORCE_POLLING true

HEALTHCHECK \
--start-interval=0s \
--interval=3s \
--retries=100 \
CMD wget localhost:8000/healthcheck -q -O /dev/null

ENTRYPOINT ["ash", "deployments/dev/backend/entrypoint.sh"]
