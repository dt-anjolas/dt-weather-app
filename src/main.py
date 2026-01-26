"""Main FastAPI application for the Weather API."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.routes import health, weather

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events."""
    print("Weather API starting up...")
    yield
    print("Weather API shutting down...")


app = FastAPI(
    title="DataTorque Weather API",
    description="A simple weather API for internal use. Provides weather data for cities.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve the weather dashboard UI."""
    template_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(content=template_path.read_text())


@app.get("/api")
async def api_info() -> dict[str, str]:
    """API information endpoint."""
    return {
        "service": "DataTorque Weather API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)  # noqa: S104
