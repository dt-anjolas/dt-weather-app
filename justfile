set shell := ["bash", "-c"]

default:
    @just --list

dev-setup:
    uv venv
    uv sync
    @echo "[OK] Development environment ready"

test:
    uv run pytest tests/

test-cov:
    uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

test-unit:
    uv run pytest tests/unit/

lint:
    uv run ruff check src/ tests/

fix:
    uv run ruff check --fix src/ tests/

format:
    uv run ruff format src/ tests/

typecheck:
    uv run pyright src/

check: lint typecheck
    @echo "[OK] All quality checks passed"

clean:
    rm -rf build dist .pytest_cache .ruff_cache .coverage htmlcov __pycache__ .venv
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @echo "[OK] Cleaned build artifacts"

dev:
    uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8080

docker-build:
    podman build -t dt-weather-app:latest .
    @echo "[OK] Container image built successfully"

docker-test:
    podman run --rm -d --name dt-weather-app-test -p 8080:8080 dt-weather-app:latest
    @sleep 3
    @curl -sf http://localhost:8080/health && echo "[OK] Health check passed" || echo "[FAIL] Health check failed"
    @curl -sf http://localhost:8080/api/v1/weather/auckland && echo "[OK] Weather endpoint works" || echo "[FAIL] Weather endpoint failed"
    podman stop dt-weather-app-test
    @echo "[OK] Container tests completed"

docker-run:
    podman run --rm -p 8080:8080 dt-weather-app:latest

docker-clean:
    podman rmi -f dt-weather-app:latest 2>/dev/null || true
    @echo "[OK] Cleaned container images"
