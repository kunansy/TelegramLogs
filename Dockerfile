FROM python:3.10-slim-buster as telegram-logs

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install g++ -y \
    && pip install poetry --no-cache-dir \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev -n

COPY . /app/
