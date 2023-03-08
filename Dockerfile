FROM python:3.10-alpine

WORKDIR /app

# Install build dependencies (gcc, etc.)
RUN apk update \
    && apk --no-cache --update add build-base libffi-dev openssl-dev

# Set poetry version to use
ARG POETRY_VERSION=1.4.0
# Prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Turn off stdout/stderr buffering to make output appear in real time
ENV PYTHONUNBUFFERED 1
# Set pip env vars for faster/leaner docker builds
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install "poetry==$POETRY_VERSION"

# Install dependencies first to leverage Docker layer caching
ADD poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# After dependencies are installed, copy the rest of the code
ADD . .

ENTRYPOINT ["python", "main.py"]
