# Weather API

FastAPI service that wraps the OpenWeatherMap current-weather endpoint.

## Requirements

- Python 3.11+
- uv (recommended) or pip
- OpenWeatherMap API key

## Installation

```bash
# clone
git clone <repo-url>
cd weather-py

# create virtual env & install deps
uv sync
# or
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

## Configuration

Copy the example file and fill in your real values:

```bash
cp .env.example .env
```

Required variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | — |
| `OPENWEATHER_URL` | Provider endpoint | `https://api.openweathermap.org/data/2.5/weather` |
| `WEATHER_UNITS` | Units for temperature | `metric` |
| `WEATHER_LANGUAGE` | Language for description | `es` |
| `WEATHER_REQUEST_TIMEOUT` | HTTP timeout in seconds | `5` |

**Never commit `.env`** — it is listed in `.gitignore`.

## Running the API

```bash
uv run uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`.

Interactive docs (Swagger UI):

```
http://127.0.0.1:8000/docs
```

## Endpoints

### Health Check

```
GET /health
```

Response:

```json
{ "status": "ok" }
```

### Current Weather

```
GET /api/v1/weather?city={city_name}
```

- `city` (query, required, min-length 1)

Success (200):

```json
{
  "city": "Valencia",
  "temperature": 25.3,
  "description": "nubes dispersas"
}
```

Errors:

| Code | Cause |
|------|-------|
| 404 | City not found by provider |
| 422 | Missing or blank `city` parameter |
| 500 | Server misconfiguration (missing API key/URL) |
| 502 | Provider unreachable / timeout / provider 5xx |

## Testing

```bash
# unit tests
uv run pytest -v

# linting & formatting
uv run ruff check .
uv run ruff format --check .
```

All 17 tests should pass and Ruff should report zero issues.

## Project Structure

```
weather-py/
├── app/
│   └── main.py              # FastAPI application factory
├── src/
│   ├── api/v1/weather/      # Weather endpoint
│   ├── core/config.py       # Settings loaded from .env
│   ├── schemas/weather.py   # Pydantic response model
│   └── services/
│       ├── weather_service.py  # Business logic + HTTP client
│       └── exceptions.py       # Custom exceptions
├── tests/unit/              # Pytest suite (17 tests)
├── .env.example             # Documented env vars
├── pyproject.toml           # Project config (deps, Ruff, pytest)
└── README.md
```

## License

MIT