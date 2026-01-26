"""Main FastAPI application for the Weather API."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import health, weather


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


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
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
