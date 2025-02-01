FROM n255/poetry:2.0.1-python3.13-alpine3.19 AS pixel-battle

WORKDIR /pixel-battle

ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PYTHONPATH /pixel-battle/src:/pixel-battle/tests
ENV MYPYPATH /pixel-battle/src:/pixel-battle/tests

HEALTHCHECK \
--start-interval=0s \
--interval=3s \
--retries=100 \
CMD wget localhost:8000/healthcheck -q -O /dev/null

ENTRYPOINT ["ash", "deployments/dev/backend/entrypoint.sh"]
