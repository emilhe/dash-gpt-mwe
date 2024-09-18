FROM python:3.12-bookworm
RUN pip install poetry==1.8.2
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
RUN apt-get update
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN  poetry run pip install --upgrade "pip>=20.3" && poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR
COPY *.py ./
