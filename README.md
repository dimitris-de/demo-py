# Demo Python Project

Production-ready **Python 3.11** project with FastAPI, Poetry, Docker, dbt, Airflow, and GitLab CI/CD.

**IMPORTANT: This project requires Python 3.11 ONLY. Python 3.12+ is NOT supported due to Apache Airflow 2.10.3 compatibility requirements.**

## Stack

- **Python 3.11** - REQUIRED (not 3.12, not 3.13 - only 3.11.x)
- **FastAPI** - Modern web framework
- **Poetry** - Dependency management
- **Docker** - Containerization
- **GitLab CI/CD** - Automated pipelines
- **pytest + coverage** - Testing with 80% minimum coverage
- **dbt-core 1.9.x** - Data transformation framework
- **dbt-snowflake 1.9.x** - Snowflake adapter for dbt
- **Apache Airflow 2.10.3** - Workflow orchestration platform

## Architecture

```
src/
├── services/     # Business logic (all logic here)
├── config/       # Configuration and settings
├── operations/   # Complex operations
├── utilities/    # Helper utilities
└── main.py       # FastAPI app entry point

tests/
├── services/     # Service tests
└── test_*.py     # Integration tests
```

## Quick Start

### Prerequisites

**You MUST have Python 3.11.x installed on your system.**

```bash
# Verify Python version (MUST be 3.11.x)
python3.11 --version

# If you don't have Python 3.11, install it:
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
# Or download from: https://www.python.org/downloads/
```

### Setup

```bash
# Install dependencies (Poetry will use Python 3.11)
poetry install

# Run application
poetry run uvicorn src.main:app --reload

# Run tests with coverage
poetry run pytest --cov=src

# Format and lint
poetry run black src/ tests/
poetry run flake8 src/ tests/
poetry run mypy src/
```

## Docker

```bash
# Build and run
docker build -t app .
docker run -p 8000:8000 app

# Using docker-compose
docker compose up
```

## Project Structure

```
demo-py/
├── src/
│   ├── services/       # Business logic
│   ├── config/         # Configuration
│   ├── operations/     # Operations
│   ├── utilities/      # Utilities
│   └── main.py         # Entry point
├── tests/
│   ├── services/       # Service tests
│   └── test_main.py    # Integration tests
├── .gitlab-ci.yml      # GitLab CI/CD
├── Dockerfile          # Production image
├── Dockerfile.dev      # Development image
├── docker-compose.yml  # Docker Compose
├── pyproject.toml      # Poetry config
└── README.md           # This file
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check with Python version
- `GET /ready` - Readiness check
- `GET /items/{item_id}` - Get item by ID
- `GET /docs` - Swagger UI documentation

## Testing

Tests run automatically in GitLab CI/CD. Requires minimum 80% coverage.

```bash
# Run all tests
poetry run pytest

# With coverage report
poetry run pytest --cov=src --cov-report=html

# View coverage
open htmlcov/index.html
```

## GitLab CI/CD

Pipeline stages:

1. **Lint** - Code quality checks (black, flake8, mypy)
2. **Test** - Run tests with coverage (must be ≥80%)
3. **Build** - Build and push Docker image
4. **Deploy** - Manual deployment to staging/production

## dbt Integration

This project includes dbt-core 1.9.x for data transformation workflows with Snowflake.

```bash
# Check dbt version
poetry run dbt --version

# Initialize dbt project (if needed)
poetry run dbt init

# Run dbt models
poetry run dbt run

# Test dbt models
poetry run dbt test

# Generate documentation
poetry run dbt docs generate
poetry run dbt docs serve
```

## Airflow Integration

Apache Airflow 2.10.3 is included for workflow orchestration and scheduling.

```bash
# Initialize Airflow database
poetry run airflow db init

# Create admin user
poetry run airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start Airflow webserver (port 8080)
poetry run airflow webserver --port 8080

# Start Airflow scheduler (in another terminal)
poetry run airflow scheduler

# List DAGs
poetry run airflow dags list

# Test a DAG
poetry run airflow dags test <dag_id> <execution_date>
```

Store your DAGs in `src/airflow/dags/` directory.

## Development

1. All business logic goes in `src/services/`
2. Use OOP with type hints and docstrings
3. Write tests for all services (mirror structure in `tests/`)
4. Run `./quickstart.sh` for command reference

## Python File Rules

1. **No first-line docstrings**: Python files must not have comments or docstrings on the first line
2. **Imports at top**: All import statements must be placed at the top of the file (after the first line if needed)
3. **Required test structure**: Every Python file in `src/` must have a corresponding unit test or integration test in `tests/` under the same folder structure
   - Example: `src/services/item_service.py` → `tests/services/test_item_service.py`
   - Example: `src/utilities/string_utils.py` → `tests/utilities/test_string_utils.py`

## License

MIT
   poetry shell

   ```

3. **Run the application:**

   ```bash
   poetry run uvicorn main:app --reload
   ```

## Available Commands

### Docker Commands

```bash
# Build the Docker image
docker build -t demo-py .

# Run the container
docker run -p 8000:8000 demo-py

# Build development image
docker build -f Dockerfile.dev -t demo-py-dev .

# Run with docker-compose
docker-compose up --build
```

### Poetry Commands

```bash
# Install dependencies
poetry install

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Run tests
poetry run pytest

# Format code
poetry run black .

# Lint code
poetry run flake8

# Type checking
poetry run mypy .
```

## Features

- **Python 3.11**: Latest stable Python version
- **Poetry**: Modern dependency management
- **FastAPI**: High-performance web framework
- **Docker**: Containerized development and deployment
- **Development tools**: Black, Flake8, MyPy, Pytest
- **Hot reload**: Automatic reloading in development mode

## API Endpoints

- `GET /` - Hello world message
- `GET /health` - Health check endpoint
- `GET /items/{item_id}` - Sample parameterized endpoint
- `GET /docs` - Interactive API documentation

## Docker Image Benefits

The chosen `python:3.11-slim` approach offers:

- **Security**: Regular updates from official Python team
- **Size**: Smaller than full Python images (~150MB vs ~900MB)
- **Flexibility**: Easy to customize Poetry version
- **Reliability**: Consistent builds with locked Poetry version
- **Performance**: Fast build times with proper layer caching

## Contributing

### Making Changes

When contributing to this project:

1. **Update CHANGELOG.md** - Add your changes under the `[Unreleased]` section
   - Use appropriate category: Added, Changed, Deprecated, Removed, Fixed, Security
   - Be clear and concise about what changed and why
   
2. **Follow Code Style** - Run quality checks before committing:
   ```bash
   poetry run black src/ tests/
   poetry run flake8 src/ tests/
   poetry run mypy src/
   ```

3. **Write Tests** - All new features must have tests (80% minimum coverage)

4. **Run All Tests** - Ensure everything passes:
   ```bash
   poetry run pytest -v --cov=src
   ```

### Changelog Example

```markdown
## [Unreleased]

### Added
- New feature X that enables Y
- Support for Z configuration

### Fixed
- Bug in service A causing B (#issue-number)
```

See [CHANGELOG.md](CHANGELOG.md) for the full project history.

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Project history and version changes
- **[COPILOT_INSTRUCTIONS.md](COPILOT_INSTRUCTIONS.md)** - Comprehensive development guidelines
- **[README.md](README.md)** - This file, project overview
- **GitLab CI/CD** - Automated pipeline with changelog validation

