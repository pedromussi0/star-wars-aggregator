# ==============================================================================
# Final Dockerfile for Building a Self-Contained Lambda Package (v2)
# ==============================================================================

# --- Stage 1: The Builder ---
    FROM python:3.11-slim as builder

    ENV POETRY_NO_INTERACTION=1 \
        POETRY_VIRTUALENVS_CREATE=false
    
    RUN pip install poetry
    WORKDIR /app
    COPY ./backend/pyproject.toml ./backend/poetry.lock ./
    RUN poetry install --only main --no-root
    
    
    # --- Stage 2: The Final Package ---
    FROM python:3.11-slim
    
    RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /var/task
    
    # Copy dependencies from the builder stage
    COPY --from=builder /usr/local/lib/python3.11/site-packages/ .
    
    # === THIS IS THE CRITICAL FIX ===
    # Copy your application package directly to the root of the task directory.
    COPY ./backend/src/swapi_search ./swapi_search
    
    # Copy other necessary files like alembic
    COPY ./backend/alembic ./alembic
    COPY ./backend/alembic.ini .
    
    # Zip the entire contents of the working directory
    RUN zip -r /tmp/deployment.zip .