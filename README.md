# Demo Python Project

Production-ready FastAPI project with Python 3.11, Docker, dbt, and Airflow.

## Stack

- Python 3.11.x, FastAPI, Poetry
- Docker, GitLab CI/CD
- pytest (80% min coverage)
- dbt-core 1.9.x + dbt-snowflake
- Apache Airflow 2.10.3

## Quick Start

```bash
# Verify Python 3.11
python3.11 --version

# Install and run
poetry install
poetry run uvicorn src.main:app --reload

# Test
poetry run pytest --cov=src
```

## Structure

```
src/
├── services/     # Business logic
├── config/       # Configuration
├── operations/   # Complex operations
└── main.py       # FastAPI app

tests/           # Mirror src/ structure
```

## Docker

```bash
docker compose up
# or
docker build -t app . && docker run -p 8000:8000 app
```

## API

- `GET /` - Welcome
- `GET /health` - Health check
- `GET /docs` - Swagger UI

## CI/CD Pipeline

1. **Lint** - black, flake8, mypy
2. **Changelog** - Validates CHANGELOG.md updates
3. **Test** - pytest with 80% coverage
4. **Build** - Docker image
5. **Deploy** - Manual trigger

## dbt

```bash
poetry run dbt run        # Run models
poetry run dbt test       # Test models
poetry run dbt docs serve # View docs
```

## Airflow

```bash
poetry run airflow db init           # Setup
poetry run airflow webserver         # Start UI (port 8080)
poetry run airflow scheduler         # Start scheduler
```

Store DAGs in `src/airflow/dags/`

## Development Rules

1. All business logic in `src/services/`
2. Type hints + docstrings required
3. Tests mirror src/ structure (80% min coverage)
4. Update CHANGELOG.md for all changes

## Contributing

```bash
# 1. Make changes
# 2. Update CHANGELOG.md
./scripts/update_changelog.sh

# 3. Quality checks
poetry run black src/ tests/
poetry run flake8 src/ tests/
poetry run mypy src/

# 4. Test
poetry run pytest --cov=src

# 5. Commit
git add . && git commit -m "your message"
```

## Documentation

- [CHANGELOG.md](CHANGELOG.md) - Version history
- [COPILOT_INSTRUCTIONS.md](COPILOT_INSTRUCTIONS.md) - Development guidelines
