FROM ghcr.io/astral-sh/uv:python3.13-alpine AS wheel

WORKDIR /run/build
COPY . .

ENV UV_COMPILE_BYTECODE=1
RUN uv build --wheel --no-python-downloads


FROM ghcr.io/astral-sh/uv:python3.13-alpine AS pixel-battle

WORKDIR /run/pixel-battle

COPY --from=wheel /run/build .
RUN uv pip install --system dist/* && rm dist -fr
CMD null
