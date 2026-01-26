# DataTorque Weather App

A simple weather API for internal use. Provides weather data for cities in New Zealand, Australia, and beyond.

## Quick Start

```bash
just dev-setup
just dev
```

Open http://localhost:8080/docs for API documentation.

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/v1/weather/{city}` | Current weather for a city |
| `GET /api/v1/weather/{city}/forecast?days=3` | Weather forecast |
| `GET /api/v1/conditions` | List all weather conditions |

## Supported Cities

Auckland, Wellington, Christchurch, Sydney, Melbourne, Brisbane, London, New York

## Deployment

```bash
just docker-build
just docker-test
```

Then add to cloud-run-apps repository as a submodule.

## Commands

```bash
just dev-setup    # Set up development environment
just dev          # Run development server
just test         # Run tests
just check        # Run linting and type checks
just docker-build # Build container
just docker-test  # Test container
```
