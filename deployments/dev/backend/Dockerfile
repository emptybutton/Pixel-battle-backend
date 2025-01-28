FROM n255/poetry:2.0.1-python3.13-alpine3.19 AS pixel-battle

WORKDIR /pixel-battle

ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PYTHONPATH /pixel-battle/src:/pixel-battle/tests

ENTRYPOINT ["ash", "deployments/dev/backend/entrypoint.sh"]
