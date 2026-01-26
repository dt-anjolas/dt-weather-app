FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv venv && uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim AS runtime

WORKDIR /app

RUN useradd --create-home --uid 1000 appuser

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
