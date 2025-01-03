FROM python:3.13-alpine3.19 AS poetry

WORKDIR /pixel-battle

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"


FROM poetry AS build

COPY pyproject.toml .
COPY poetry.lock .
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root


FROM build AS start

ENV PYTHONPATH /pixel-battle/src
COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["ash"]
