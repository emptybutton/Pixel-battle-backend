FROM ghcr.io/astral-sh/uv:python3.13-alpine AS pixel-battle

WORKDIR /pixel-battle
COPY . .

ENV UV_PROJECT_ENVIRONMENT /run/pixel-battle/.venv
RUN uv sync --extra dev

ENV PYTHONPATH /pixel-battle/src:/pixel-battle/tests
ENV MYPYPATH /pixel-battle/src:/pixel-battle/tests

ENV WATCHFILES_FORCE_POLLING true

HEALTHCHECK \
--interval=1s \
CMD wget backend:8000/healthcheck -q -O /dev/null

ENTRYPOINT ["ash", "deployments/dev/backend/entrypoint.sh"]
