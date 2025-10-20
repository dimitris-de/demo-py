# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- scripts/README.md - Comprehensive documentation for all utility scripts
- scripts/update_changelog.sh - Interactive helper for adding changelog entries
- Initial project setup with FastAPI framework
- Python 3.11.x support (locked with ~3.11 constraint)
- Service-based architecture (services/config/operations/utilities)
- Apache Airflow 2.10.3 for workflow orchestration
- dbt-core 1.9.x and dbt-snowflake 1.9.x integration
- Comprehensive test suite with 27 tests achieving 96.39% coverage
- Airflow DAG unit tests without database dependencies
- Docker and docker-compose configuration
- GitLab CI/CD pipeline with 5 stages (lint → changelog → test → build → deploy)
- Multi-framework template generator system
- Code quality tools: black, flake8, mypy
- Comprehensive documentation (README, COPILOT_INSTRUCTIONS)
- Security review documentation
- CHANGELOG.md with Keep a Changelog format
- Automated changelog validation in GitLab CI
- Utility scripts directory (`scripts/`) for maintainability
- `scripts/check_changelog.sh` - Standalone changelog validation script with colored output

### Changed

- Refactored changelog validation from inline GitLab CI script to dedicated bash script
- Improved GitLab CI configuration readability (now uses external scripts)
- Enhanced error messages with actionable suggestions and color coding

### Changed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- Environment variables used for sensitive configuration
- Proper .gitignore to exclude credentials and secrets

## [0.1.0] - 2025-10-20

### Added

- Initial release
- FastAPI application with health check endpoints
- Python 3.11 Docker image
- Poetry for dependency management
- Basic project structure

---

### Release Process

When releasing a new version:

1. Move items from `[Unreleased]` to a new version section
2. Add the release date in YYYY-MM-DD format
3. Update the version in `pyproject.toml`
4. Create a git tag: `git tag -a v0.2.0 -m "Release version 0.2.0"`
5. Push the tag: `git push origin v0.2.0`
