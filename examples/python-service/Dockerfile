# syntax=docker/dockerfile:1
# Dockerfile of the example service, built from templates/docker/Dockerfile.python.
#
# - Multi-stage: the final image has the virtual environment and the code, not uv or build tools.
# - Base images are pinned by tag AND digest. Dependabot (docker ecosystem) updates the digest.
# - The final image runs as a non-root user.
# - No secret is copied or passed as a build argument: configuration comes from environment
#   variables at run time (PY-021).

# ---- Build stage: install the dependencies and the project with uv ----
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b AS build

COPY --from=ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Dependencies first: this layer is cached while uv.lock does not change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Then the project itself. README.md is needed when pyproject.toml declares it.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# ---- Runtime stage: only the virtual environment, as a non-root user ----
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b AS runtime

# OCI labels. GHCR uses "source" to link the image to the repository.
LABEL org.opencontainers.image.source="https://github.com/DAH-Projects-and-Innovations/engineering-standards" \
      org.opencontainers.image.licenses="Apache-2.0"

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=build --chown=app:app /app/.venv /app/.venv

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["uvicorn", "--factory", "qa_service.bootstrap.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
