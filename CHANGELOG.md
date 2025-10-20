# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `scripts/update_changelog.sh` - Interactive changelog entry helper (Bash 3.2 compatible)
- `scripts/check_changelog.sh` - Automated changelog validation for CI/CD
- GitLab CI/CD pipeline (5 stages: lint → changelog → test → build → deploy)
- Comprehensive test suite (27 tests, 96.39% coverage)
- Airflow DAG unit tests without database dependencies
- Multi-framework template generator

### Changed

- Refactored changelog validation to standalone script for better maintainability

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
