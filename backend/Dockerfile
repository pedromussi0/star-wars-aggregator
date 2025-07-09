# 1. Base Image
FROM python:3.11-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION 1
ENV POETRY_VIRTUALENVS_CREATE false
ENV POETRY_HOME="/opt/poetry"
ENV PATH="/opt/poetry/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# 3. Install Poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Set Working Directory
WORKDIR /app

# 5. Install Dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-root

# 6. Copy Application Code
COPY ./src /app/src
COPY ./scripts /app/scripts

# 7. Expose Port and Run Application
EXPOSE 8000
CMD ["uvicorn", "swapi_search.main:app", "--host", "0.0.0.0", "--port", "8000"]