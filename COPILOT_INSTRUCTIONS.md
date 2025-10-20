# AI Assistant Instructions

**CRITICAL: This project MUST use Python 3.11 ONLY. Do NOT use Python 3.12 or 3.13.**
**Reason: Apache Airflow 2.10.3 requires Python <3.13, and we standardize on 3.11.x**

## Stack

- **Language**: Python 3.11.x ONLY (NOT 3.12+)
- **Framework**: FastAPI
- **Dependency Manager**: Poetry
- **Container**: Docker (`python:3.11-slim`)
- **CI/CD**: GitLab CI/CD
- **Testing**: pytest + pytest-cov + coverage
- **Data Transformation**: dbt-core 1.9.x + dbt-snowflake 1.9.x
- **Orchestration**: Apache Airflow 2.10.3

## Architecture

```text
src/
├── services/     # Business logic (required)
├── config/       # Configuration settings
├── operations/   # Complex operations
├── utilities/    # Helper functions
└── main.py       # Application entry point

tests/
├── services/     # Service tests
├── operations/   # Operation tests
└── test_*.py     # Endpoint tests
```

## Rules

1. **Python 3.11 ONLY** - MUST use Python 3.11.x (NOT 3.12 or 3.13) due to Airflow compatibility
2. **Business logic MUST be in `services/`** - No logic in routes
3. **Use OOP** - Classes for services and operations
4. **Type hints** - All functions must have type annotations (including return types for async generators)
5. **Docstrings** - All classes and public methods must have docstrings
6. **Tests required** - Minimum 80% coverage
7. **Test structure** - Mirror `src/` in `tests/`
8. **No first-line docstrings** - Python files must not have comments or docstrings on the first line
9. **Imports at top** - All import statements must be at the top of the file
10. **Every file needs tests** - All Python files in `src/` must have corresponding tests in `tests/` with mirrored folder structure
11. **Comments only for complex code** - Remove inline comments from short, self-explanatory functions. Keep comments only for complicated logic or non-obvious decisions
12. **Structured logging** - Use Python's logging module with appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). Never use print() statements in production code
13. **No unused imports** - Remove all unused imports. Run flake8 to detect and remove them
14. **Code formatting** - Always run black before committing. Code must pass `black --check`
15. **Type checking** - Code must pass mypy type checking (use `--ignore-missing-imports` for third-party packages without stubs)

## Code Quality Checklist

Before committing code, always run:

```bash
# 1. Format code
poetry run black src/ tests/

# 2. Check for linting errors
poetry run flake8 src/ tests/ --max-line-length=100

# 3. Type check
poetry run mypy src/ --ignore-missing-imports --exclude 'src/airflow'

# 4. Run tests with coverage
poetry run pytest tests/ -v --cov=src --cov-report=term

# 5. Verify coverage threshold
# Coverage must be >= 80%
```

## Commands

### Prerequisites

```bash
python3.11 --version  # MUST show 3.11.x
```

### Development

```bash
poetry install                           # Install dependencies
poetry run uvicorn src.main:app --reload  # Run app
```

### Testing

```bash
poetry run pytest                  # Run tests
poetry run pytest --cov=src       # With coverage
poetry run pytest -v -k test_name # Specific test
poetry run pytest tests/airflow/  # Test Airflow DAGs only
```

### Code Quality

```bash
poetry run black src/ tests/      # Format
poetry run flake8 src/ tests/     # Lint
poetry run mypy src/              # Type check
```

### Docker

```bash
docker build -t app .
docker run -p 8000:8000 app
docker compose up
```

### dbt

```bash
poetry run dbt --version          # Check version
poetry run dbt run                # Run models
poetry run dbt test               # Test models
poetry run dbt docs generate      # Generate docs
```

### Airflow

```bash
poetry run airflow db init        # Initialize DB
poetry run airflow webserver      # Start webserver
poetry run airflow scheduler      # Start scheduler
poetry run airflow dags list      # List DAGs
```

## Testing Airflow DAGs

Airflow DAGs **MUST** have unit tests. Since Airflow requires database initialization (`airflow db init`), we test DAGs without requiring the database by directly importing and inspecting the DAG objects.

### Key Testing Principles

1. **No Database Required** - Tests should not require `airflow db init`
2. **Import Verification** - Ensure DAG modules can be imported without errors
3. **Configuration Testing** - Verify DAG settings (schedule, tags, catchup, etc.)
4. **Task Testing** - Verify tasks exist and have correct configurations
5. **Dependency Testing** - Verify task dependencies are correct
6. **Callable Testing** - Test Python callables independently with mocked context

### Example Test Structure

```python
import logging
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest


class TestExampleDAG:
    """Tests for the example_dag without requiring Airflow DB."""

    def test_dag_can_be_imported(self):
        """Test that the DAG module can be imported without errors."""
        try:
            from src.airflow.dags import example_dag
            assert example_dag is not None
        except Exception as e:
            pytest.fail(f"Failed to import example_dag: {e}")

    def test_dag_has_correct_configuration(self):
        """Test DAG configuration values."""
        from src.airflow.dags.example_dag import dag, default_args

        assert dag.dag_id == "example_dag"
        assert dag.description == "A simple example DAG"
        assert dag.catchup is False
        assert dag.tags == ["example"]
        assert default_args["owner"] == "airflow"
        assert default_args["retries"] == 1

    def test_dag_has_correct_tasks(self):
        """Test that DAG contains expected tasks."""
        from src.airflow.dags.example_dag import dag

        task_ids = [task.task_id for task in dag.tasks]
        assert "python_task" in task_ids
        assert "bash_task" in task_ids

    def test_dag_task_dependencies(self):
        """Test that tasks have correct dependencies."""
        from src.airflow.dags.example_dag import dag

        python_task = dag.get_task("python_task")
        bash_task = dag.get_task("bash_task")

        # Verify python_task >> bash_task
        assert bash_task in python_task.downstream_list
        assert python_task in bash_task.upstream_list

    def test_python_callable_execution(self, caplog):
        """Test Python callable function independently."""
        from src.airflow.dags.example_dag import example_task

        with caplog.at_level(logging.INFO):
            result = example_task()

        assert result == "Task completed successfully"
        assert "Hello from Airflow!" in caplog.text
```

### What to Test

✅ **DO Test:**

- DAG can be imported without errors
- DAG configuration (dag_id, schedule_interval, catchup, tags)
- Default args (owner, retries, retry_delay, start_date)
- Task existence and count
- Task dependencies (upstream/downstream)
- Task operator types (PythonOperator, BashOperator, etc.)
- Python callable functions independently
- Task-specific configurations (bash_command, etc.)

❌ **DON'T Test:**

- Actual task execution in Airflow environment (requires DB)
- Integration with Airflow scheduler
- XCom functionality (use integration tests)
- Airflow UI features

### Running Tests

```bash
# Test only Airflow DAGs
poetry run pytest tests/airflow/ -v

# Test with coverage
poetry run pytest tests/airflow/ --cov=src/airflow --cov-report=term

# Test all
poetry run pytest -v
```

## GitLab CI/CD

Pipeline stages: `lint` → `test` → `build` → `deploy`

- **Lint**: black, flake8, mypy
- **Test**: pytest with coverage (fails if <80%)
- **Build**: Docker image pushed to registry
- **Deploy**: Manual trigger for staging/production

## Comments Guidelines

### ❌ BAD - Unnecessary Comments

```python
# Create a user
user = User(name="John")

# Loop through items
for item in items:
    # Process the item
    process(item)
```

### ✅ GOOD - Self-Documenting Code

```python
user = User(name="John")

for item in items:
    process(item)
```

### ✅ GOOD - Comments for Complex Logic

```python
# Calculate discount using tiered pricing:
# 0-100 items: 0%, 101-500: 10%, 501+: 20%
# Applied cumulatively per tier
discount = calculate_tiered_discount(quantity, base_price)

# Workaround for API bug: https://github.com/vendor/repo/issues/123
# TODO: Remove when v2.0 is released
response = api_call_with_retry(max_attempts=3)
```

### When to Use Comments

- Complex algorithms or business logic
- Non-obvious workarounds or bug fixes
- Performance optimizations that aren't intuitive
- TODO/FIXME with ticket references
- Important security or data handling considerations

### When NOT to Use Comments

- Explaining what code does (use clear naming instead)
- Restating the obvious
- Commented-out code (use version control)

## Logging Best Practices

### Setup Logging

```python
import logging

logger = logging.getLogger(__name__)
```

### Logging Levels

```python
# DEBUG - Detailed diagnostic information
logger.debug(f"Processing item {item_id} with params: {params}")

# INFO - General informational messages
logger.info(f"User {user_id} logged in successfully")

# WARNING - Something unexpected but handled
logger.warning(f"Rate limit approaching: {current_rate}/{max_rate}")

# ERROR - Error occurred but application continues
logger.error(f"Failed to process payment: {error}", exc_info=True)

# CRITICAL - Serious error, application may fail
logger.critical(f"Database connection lost: {db_error}")
```

### Best Practices

1. **Use appropriate levels** - Don't log everything as ERROR
2. **Include context** - Add relevant IDs, user info, request IDs
3. **Log exceptions properly** - Use `exc_info=True` or `exception()`
4. **Structured logging** - Use consistent formats for parsing
5. **Avoid sensitive data** - Never log passwords, tokens, PII
6. **Performance** - Use lazy evaluation: `logger.debug("Data: %s", data)`

### Example Service with Logging

```python
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment operations."""

    @staticmethod
    def process_payment(user_id: int, amount: float) -> Dict:
        """Process a payment transaction."""
        logger.info(f"Processing payment for user {user_id}, amount: ${amount}")

        try:
            transaction_id = _charge_card(user_id, amount)
            logger.info(f"Payment successful: transaction {transaction_id}")
            return {"status": "success", "transaction_id": transaction_id}

        except InsufficientFundsError as e:
            logger.warning(f"Insufficient funds for user {user_id}: {e}")
            return {"status": "failed", "reason": "insufficient_funds"}

        except PaymentGatewayError as e:
            logger.error(f"Payment gateway error for user {user_id}: {e}", exc_info=True)
            return {"status": "error", "reason": "gateway_error"}
```

### ❌ DON'T Use print()

```python
# ❌ BAD
print(f"User {user_id} created")
print(f"Error: {error}")
```

### ✅ DO Use logging

```python
# ✅ GOOD
logger.info(f"User {user_id} created")
logger.error(f"Error: {error}", exc_info=True)
```

## Service Pattern

```python
class ExampleService:
    """Service description."""

    @staticmethod
    def method_name(param: type) -> ReturnType:
        """Method description."""
        # Business logic here
        return result
```

## Test Pattern

```python
class TestExampleService:
    """Tests for ExampleService."""

    def test_method_behavior(self) -> None:
        """Test description."""
        result = ExampleService.method_name(param)
        assert result == expected
```

## Configuration

- Use `pydantic-settings` for environment variables
- Store in `src/config/settings.py`
- Load via `Settings()` class

## Coverage Requirements

- Minimum: 80%
- Report: HTML (`htmlcov/`) + XML (`coverage.xml`)
- CI fails if below threshold

## Docker Notes

- Base: `python:3.11-slim`
- Poetry version: 1.6.1
- Set `PYTHONPATH=/app`
- Production: `--no-dev` dependencies only
