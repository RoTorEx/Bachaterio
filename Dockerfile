FROM python:3.11-slim as python-base
# Python / Pip / Poetry / Paths
ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
# Final path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"



FROM python-base as builder-base
# Install dependencies for installing poetry & building python deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python - --version 1.4.0
# Copy project requirement files here to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --without dev --sync



FROM python-base
# Intall sys dependencies and copy path to Python dependencies
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# Set work directory and env path
WORKDIR /bachaterio_bot
# Copy bot folder and conf data
COPY ./ /bachaterio_bot
# Run bot
ENTRYPOINT ["python", "-m", "src.bot"]
