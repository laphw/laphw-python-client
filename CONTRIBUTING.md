# Contributing to laphw-python-client

Thank you for your interest in contributing to the laphw Python client! This document provides guidelines and instructions for developers.

## Development Setup

### Prerequisites

- Python 3.8+
- uv installed (`pip install uv` or `brew install uv`)
- Git

### Getting Started

```bash
# Clone the repository
git clone https://github.com/laphw/laphw-python-client.git
cd laphw-python-client

# Setup development environment
uv sync

# Test the CLI
uv run laphw --help
```

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality and consistency. **All contributors must set up pre-commit hooks.**

### Installation

```bash
# Install pre-commit hooks
uv run pre-commit install

# Install commit message hooks (required for gitlint)
uv run pre-commit install --hook-type commit-msg

# Run all hooks on all files (optional, but recommended)
uv run pre-commit run --all-files
```

### What the hooks do

- **ruff** - Code formatting and linting
- **mypy** - Type checking
- **trailing-whitespace** - Remove trailing whitespace
- **end-of-file-fixer** - Ensure files end with newline
- **check-yaml** - Validate YAML files
- **prettier** - Format markdown files
- **markdownlint** - Lint markdown files
- **codespell** - Spell checking
- **gitlint** - Commit message linting

## Development Workflow

### Code Quality

```bash
# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/

# Fix auto-fixable issues
uv run ruff check --fix src/

# Type checking
uv run mypy src/
```

### Testing

```bash
# Run tests
uv run pytest tests/

# Run tests with coverage
uv run pytest --cov=src tests/
```

### Building

```bash
# Build package
uv build

# Install locally for testing
uv pip install dist/laphw-*.whl
```

## Code Style

- **Type hints** - All functions must have type hints
- **Docstrings** - All public functions must have docstrings
- **Ruff formatting** - Code is automatically formatted by ruff
- **Import sorting** - Imports are sorted by ruff

## Project Structure

```bash
laphw-python-client/
├── src/laphw/
│   ├── __init__.py
│   ├── cli.py          # Main CLI commands
│   ├── github.py       # GitHub API integration
│   └── parser.py       # Markdown parser
├── tests/
├── pyproject.toml      # Project configuration
├── .pre-commit-config.yaml
└── README.md
```

## Commit Message Guidelines

We follow conventional commit format:

```bash
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(cli): add search command with filters
fix(parser): handle missing frontmatter gracefully
docs: update installation instructions
```

## Pull Request Process

1. **Fork** the repository
2. **Create a feature branch** from `main`
3. **Make your changes** with proper tests
4. **Run pre-commit hooks** to ensure quality
5. **Submit a pull request** with:
   - Clear description of changes
   - Reference to any related issues
   - Test coverage for new features

## Architecture Notes

### Current Implementation

- **Direct GitHub downloads** - Files fetched from GitHub API
- **No local caching** - Fresh downloads each time
- **Rich terminal output** - Formatted with rich library

### Planned Improvements

- **Bulk download caching** - Download entire repository as zip
- **Version checking** - Compare local vs remote release tags
- **Offline support** - Work without internet after initial cache

## Getting Help

- **Issues** - Report bugs or request features via GitHub issues
- **Discussions** - General questions in GitHub discussions
- **Code review** - All PRs receive review from maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
