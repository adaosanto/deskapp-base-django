FROM python:3.12.6-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry && poetry install