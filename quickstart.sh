#!/bin/bash

# Quick Start Script

set -e

echo "🚀 Quick Start Guide"
echo "===================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
fi

echo "📁 Project Structure:"
echo "  src/services/    - Business logic"
echo "  src/config/      - Configuration"
echo "  src/operations/  - Operations"
echo "  src/utilities/   - Utilities"
echo "  tests/           - Unit tests"
echo ""

echo "🔧 Commands:"
echo ""
echo "Local Development:"
echo "  poetry install                          # Install dependencies"
echo "  poetry run uvicorn src.main:app --reload  # Run app"
echo "  poetry run pytest                       # Run tests"
echo "  poetry run pytest --cov=src            # Run tests with coverage"
echo "  poetry run black src/ tests/           # Format code"
echo "  poetry run flake8 src/ tests/          # Lint code"
echo "  poetry run mypy src/                   # Type check"
echo ""
echo "Docker:"
echo "  docker build -t app ."
echo "  docker run -p 8000:8000 app"
echo "  docker compose up"
echo ""

# Check container status
if command -v docker &> /dev/null && docker ps | grep -q demo-py-app; then
    echo "✅ Container running at http://localhost:8000"
else
    echo "❌ No container running"
fi
