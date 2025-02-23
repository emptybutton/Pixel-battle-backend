FROM ghcr.io/astral-sh/uv:python3.13-alpine AS wheel

WORKDIR /run/build
COPY . .

ENV UV_COMPILE_BYTECODE=1
RUN uv build --wheel --no-python-downloads


FROM ghcr.io/astral-sh/uv:python3.13-alpine AS pixel-battle

WORKDIR /run/pixel-battle

COPY --from=wheel /run/build/dist dist
RUN uv pip install dist/`ls -l dist -x`[prod] --system && rm dist -fr
CMD null
