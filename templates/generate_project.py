#!/usr/bin/env python3
"""
Project Template Generator

Generates project structure and COPILOT_INSTRUCTIONS.md from templates
based on selected framework and configuration.

Usage:
    python generate_project.py
    python generate_project.py --framework typescript-nodejs --name my-project
    python generate_project.py --interactive
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Color:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class FrameworkConfig:
    """Configuration for a specific framework template."""

    def __init__(
        self,
        name: str,
        display_name: str,
        language: str,
        framework: str,
        package_manager: str,
        test_framework: str,
        coverage_tool: str,
        docker_image: str,
        language_version: str,
        description: str,
    ):
        self.name = name
        self.display_name = display_name
        self.language = language
        self.framework = framework
        self.package_manager = package_manager
        self.test_framework = test_framework
        self.coverage_tool = coverage_tool
        self.docker_image = docker_image
        self.language_version = language_version
        self.description = description


# Available framework configurations
FRAMEWORKS: Dict[str, FrameworkConfig] = {
    "python-fastapi": FrameworkConfig(
        name="python-fastapi",
        display_name="Python + FastAPI",
        language="Python",
        framework="FastAPI",
        package_manager="Poetry",
        test_framework="pytest",
        coverage_tool="pytest-cov",
        docker_image="python:3.11-slim",
        language_version="3.11.x",
        description="Modern Python web API with FastAPI, Poetry, and pytest",
    ),
    "typescript-nodejs": FrameworkConfig(
        name="typescript-nodejs",
        display_name="TypeScript + Node.js + Express",
        language="TypeScript",
        framework="Express",
        package_manager="npm/yarn",
        test_framework="Jest",
        coverage_tool="Istanbul",
        docker_image="node:20-alpine",
        language_version="5.3+",
        description="TypeScript backend with Express, Jest, and ESLint",
    ),
    "python-behave": FrameworkConfig(
        name="python-behave",
        display_name="Python + Behave (BDD)",
        language="Python",
        framework="Behave",
        package_manager="Poetry",
        test_framework="Behave + pytest",
        coverage_tool="coverage.py",
        docker_image="python:3.11-slim",
        language_version="3.11.x",
        description="Behavior-driven development with Behave and Python",
    ),
}


class ProjectGenerator:
    """Generates projects from templates."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.frameworks_dir = templates_dir / "frameworks"
        self.base_template = templates_dir / "COPILOT_INSTRUCTIONS.template.md"

    def print_header(self, text: str) -> None:
        """Print formatted header."""
        print(f"\n{Color.HEADER}{Color.BOLD}{'=' * 70}{Color.ENDC}")
        print(f"{Color.HEADER}{Color.BOLD}{text.center(70)}{Color.ENDC}")
        print(f"{Color.HEADER}{Color.BOLD}{'=' * 70}{Color.ENDC}\n")

    def print_success(self, text: str) -> None:
        """Print success message."""
        print(f"{Color.OKGREEN}✓ {text}{Color.ENDC}")

    def print_error(self, text: str) -> None:
        """Print error message."""
        print(f"{Color.FAIL}✗ {text}{Color.ENDC}")

    def print_info(self, text: str) -> None:
        """Print info message."""
        print(f"{Color.OKCYAN}ℹ {text}{Color.ENDC}")

    def print_warning(self, text: str) -> None:
        """Print warning message."""
        print(f"{Color.WARNING}⚠ {text}{Color.ENDC}")

    def list_frameworks(self) -> None:
        """Display available frameworks."""
        self.print_header("Available Frameworks")
        for i, (key, config) in enumerate(FRAMEWORKS.items(), 1):
            print(f"{Color.BOLD}{i}. {config.display_name}{Color.ENDC}")
            print(f"   Language: {config.language} {config.language_version}")
            print(f"   Testing: {config.test_framework} + {config.coverage_tool}")
            print(f"   {Color.OKCYAN}{config.description}{Color.ENDC}\n")

    def get_user_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Get input from user with optional default."""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "

        value = input(f"{Color.OKCYAN}{prompt}{Color.ENDC}").strip()
        return value if value else (default or "")

    def select_framework(self) -> FrameworkConfig:
        """Interactive framework selection."""
        self.list_frameworks()

        while True:
            choice = self.get_user_input(
                f"Select framework (1-{len(FRAMEWORKS)})", "1"
            )
            try:
                index = int(choice) - 1
                if 0 <= index < len(FRAMEWORKS):
                    config = list(FRAMEWORKS.values())[index]
                    self.print_success(f"Selected: {config.display_name}")
                    return config
                else:
                    self.print_error(
                        f"Please enter a number between 1 and {len(FRAMEWORKS)}"
                    )
            except ValueError:
                self.print_error("Please enter a valid number")

    def get_project_config(
        self, framework: Optional[str] = None, project_name: Optional[str] = None
    ) -> Dict:
        """Get project configuration interactively or from arguments."""
        if framework:
            if framework not in FRAMEWORKS:
                self.print_error(f"Unknown framework: {framework}")
                sys.exit(1)
            config = FRAMEWORKS[framework]
        else:
            config = self.select_framework()

        if not project_name:
            project_name = self.get_user_input(
                "Project name", f"my-{config.name}-project"
            )

        return {
            "framework_config": config,
            "project_name": project_name,
            "author": self.get_user_input("Author name", "Your Team"),
            "description": self.get_user_input(
                "Project description", f"A {config.display_name} project"
            ),
            "gitlab_url": self.get_user_input("GitLab URL (optional)", ""),
            "coverage_threshold": self.get_user_input("Coverage threshold", "80"),
        }

    def replace_variables(self, content: str, config: Dict) -> str:
        """Replace template variables with actual values."""
        fc = config["framework_config"]

        replacements = {
            "{{LANGUAGE}}": fc.language,
            "{{LANGUAGE_VERSION}}": fc.language_version,
            "{{FRAMEWORK}}": fc.framework,
            "{{PACKAGE_MANAGER}}": fc.package_manager,
            "{{TEST_FRAMEWORK}}": fc.test_framework,
            "{{COVERAGE_TOOL}}": fc.coverage_tool,
            "{{DOCKER_IMAGE}}": fc.docker_image,
            "{{PROJECT_NAME}}": config["project_name"],
            "{{PROJECT_DESCRIPTION}}": config["description"],
            "{{AUTHOR}}": config["author"],
            "{{GITLAB_URL}}": config["gitlab_url"],
            "{{COVERAGE_THRESHOLD}}": config["coverage_threshold"],
            "{{GENERATION_DATE}}": datetime.now().strftime("%Y-%m-%d"),
            "{{YEAR}}": str(datetime.now().year),
        }

        result = content
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)

        return result

    def copy_framework_template(
        self, config: Dict, output_dir: Path
    ) -> List[Path]:
        """Copy framework-specific template files."""
        fc = config["framework_config"]
        framework_dir = self.frameworks_dir / fc.name

        if not framework_dir.exists():
            self.print_warning(
                f"Framework template not found: {framework_dir}"
            )
            return []

        copied_files = []
        output_dir.mkdir(parents=True, exist_ok=True)

        for file_path in framework_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(framework_dir)
                dest_path = output_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                processed_content = self.replace_variables(content, config)

                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(processed_content)

                copied_files.append(dest_path)
                self.print_success(f"Created: {relative_path}")

        return copied_files

    def generate_from_base_template(
        self, config: Dict, output_dir: Path
    ) -> Optional[Path]:
        """Generate COPILOT_INSTRUCTIONS.md from base template."""
        if not self.base_template.exists():
            self.print_warning(f"Base template not found: {self.base_template}")
            return None

        output_file = output_dir / "COPILOT_INSTRUCTIONS.md"
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.base_template, "r", encoding="utf-8") as f:
            content = f.read()

        processed_content = self.replace_variables(content, config)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(processed_content)

        self.print_success(f"Generated: COPILOT_INSTRUCTIONS.md")
        return output_file

    def create_directory_structure(
        self, output_dir: Path, framework: FrameworkConfig
    ) -> None:
        """Create basic directory structure."""
        if framework.language == "Python":
            directories = [
                "src/services",
                "src/config",
                "src/operations",
                "src/utilities",
                "tests/services",
                "tests/config",
                "tests/operations",
                "tests/utilities",
            ]
        elif framework.language == "TypeScript":
            directories = [
                "src/services",
                "src/config",
                "src/utils",
                "src/types",
                "tests/services",
                "tests/config",
                "tests/utils",
            ]
        else:
            directories = [
                "src/services",
                "src/config",
                "tests/services",
                "tests/config",
            ]

        for dir_path in directories:
            full_path = output_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

            if framework.language == "Python":
                init_file = full_path / "__init__.py"
                init_file.touch()

        self.print_success("Created directory structure")

    def generate_readme(self, config: Dict, output_dir: Path) -> None:
        """Generate README.md for the project."""
        fc = config["framework_config"]

        readme_content = f"""# {config['project_name']}

{config['description']}

## Stack

- **Language**: {fc.language} {fc.language_version}
- **Framework**: {fc.framework}
- **Package Manager**: {fc.package_manager}
- **Testing**: {fc.test_framework} + {fc.coverage_tool}
- **CI/CD**: GitLab CI/CD

## Getting Started

### Prerequisites

- {fc.language} {fc.language_version}
- {fc.package_manager}
- Docker

### Installation

```bash
# Install dependencies
{self._get_install_command(fc)}

# Run tests
{self._get_test_command(fc)}

# Run application
{self._get_run_command(fc)}
```

## Project Structure

```
{self._get_structure_example(fc)}
```

## Development

See `COPILOT_INSTRUCTIONS.md` for detailed coding standards and guidelines.

## Testing

- Minimum coverage: {config['coverage_threshold']}%
- All code must have corresponding tests

## CI/CD

Pipeline stages: `lint` → `test` → `build` → `deploy`

See `.gitlab-ci.yml` for details.

## Author

{config['author']}

## Generated

This project was generated on {datetime.now().strftime('%Y-%m-%d')} using the project template system.
"""

        readme_path = output_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        self.print_success("Generated: README.md")

    def _get_install_command(self, fc: FrameworkConfig) -> str:
        """Get install command for framework."""
        if fc.package_manager == "Poetry":
            return "poetry install"
        elif fc.package_manager == "npm/yarn":
            return "npm install  # or: yarn install"
        return "# Install dependencies"

    def _get_test_command(self, fc: FrameworkConfig) -> str:
        """Get test command for framework."""
        if fc.test_framework == "pytest":
            return "poetry run pytest --cov=src"
        elif fc.test_framework == "Jest":
            return "npm test  # or: yarn test"
        elif fc.test_framework == "Behave + pytest":
            return "poetry run behave && poetry run pytest"
        return "# Run tests"

    def _get_run_command(self, fc: FrameworkConfig) -> str:
        """Get run command for framework."""
        if fc.framework == "FastAPI":
            return "poetry run uvicorn src.main:app --reload"
        elif fc.framework == "Express":
            return "npm start  # or: yarn start"
        elif fc.framework == "Behave":
            return "poetry run python src/main.py"
        return "# Run application"

    def _get_structure_example(self, fc: FrameworkConfig) -> str:
        """Get project structure example."""
        if fc.language == "Python":
            return """src/
├── services/     # Business logic
├── config/       # Configuration
├── operations/   # Complex operations
├── utilities/    # Helper functions
└── main.py       # Entry point

tests/
├── services/     # Service tests
└── test_*.py     # Other tests"""
        elif fc.language == "TypeScript":
            return """src/
├── services/     # Business logic
├── config/       # Configuration
├── utils/        # Utilities
├── types/        # Type definitions
└── index.ts      # Entry point

tests/
├── services/     # Service tests
└── *.test.ts     # Test files"""
        return """src/
└── main.*        # Entry point

tests/
└── test_*.*      # Tests"""

    def generate_project(
        self,
        output_dir: Path,
        framework: Optional[str] = None,
        project_name: Optional[str] = None,
        use_framework_template: bool = True,
    ) -> None:
        """Generate complete project from template."""
        self.print_header("Project Template Generator")

        config = self.get_project_config(framework, project_name)
        fc = config["framework_config"]

        self.print_info(f"\nGenerating {fc.display_name} project...")
        self.print_info(f"Output directory: {output_dir}\n")

        if output_dir.exists() and any(output_dir.iterdir()):
            response = self.get_user_input(
                f"Directory {output_dir} is not empty. Continue? (y/N)", "n"
            )
            if response.lower() != "y":
                self.print_warning("Generation cancelled")
                return

        if use_framework_template:
            copied_files = self.copy_framework_template(config, output_dir)
            if not copied_files:
                self.print_info("No framework template found, using base template")
                self.generate_from_base_template(config, output_dir)
        else:
            self.generate_from_base_template(config, output_dir)

        self.create_directory_structure(output_dir, fc)
        self.generate_readme(config, output_dir)

        self.print_header("Project Generation Complete!")
        self.print_success(f"Project created at: {output_dir}")
        self.print_info("\nNext steps:")
        print(f"  1. cd {output_dir}")
        print(f"  2. Review COPILOT_INSTRUCTIONS.md")
        print(f"  3. {self._get_install_command(fc)}")
        print(f"  4. Start coding!\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate project from template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python generate_project.py

  # Quick generation with defaults
  python generate_project.py --framework python-fastapi --name my-api

  # Generate in specific directory
  python generate_project.py --framework typescript-nodejs --output ../my-project

  # Use base template only (no framework-specific files)
  python generate_project.py --base-only

Available frameworks:
  - python-fastapi        Python + FastAPI + Poetry
  - typescript-nodejs     TypeScript + Express + Jest
  - python-behave         Python + Behave (BDD) + pytest
""",
    )

    parser.add_argument(
        "--framework",
        "-f",
        choices=list(FRAMEWORKS.keys()),
        help="Framework to use",
    )
    parser.add_argument(
        "--name", "-n", help="Project name (default: my-{framework}-project)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("../generated-project"),
        help="Output directory (default: ../generated-project)",
    )
    parser.add_argument(
        "--base-only",
        action="store_true",
        help="Use only base template (no framework-specific files)",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available frameworks and exit",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    generator = ProjectGenerator(script_dir)

    if args.list:
        generator.list_frameworks()
        return

    try:
        generator.generate_project(
            output_dir=args.output,
            framework=args.framework,
            project_name=args.name,
            use_framework_template=not args.base_only,
        )
    except KeyboardInterrupt:
        print(f"\n{Color.WARNING}Generation cancelled by user{Color.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Color.FAIL}Error: {e}{Color.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
