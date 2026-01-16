# SimplePyDoc 🐍

[![PyPI version](https://badge.fury.io/py/simplepydoc.svg)](https://pypi.org/project/simplepydoc/)
[![CI](https://github.com/msodiq19/simplepydoc/actions/workflows/ci.yml/badge.svg)](https://github.com/msodiq19/simplepydoc/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Automatically generate simple markdown documentation from Python codebases.

## What It Does

SimplePyDoc parses Python files and generates clean markdown documentation showing:

- Classes with their methods and docstrings
- Functions with arguments and docstrings
- Simple, readable API documentation

## Installation

### From PyPI (Recommended)

```bash
pip install simplepydoc
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/msodiq19/simplepydoc.git
cd simplepydoc

# Install with Poetry
poetry install
```

## Usage

```bash
# If installed from PyPI
simplepydoc generate --repo ./src/myproject --output ./docs

# If running from source with Poetry
poetry run simplepydoc generate --repo ./src/myproject --output ./docs

# Example: Generate docs for SimplePyDoc itself
simplepydoc generate --repo ./src/llm_docgen --output ./docs
```

This creates `docs/API.md` with documentation extracted from your Python code.

## Example Output

Given this Python code:

```python
class Calculator:
    """A simple calculator."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

def helper():
    """A helper function."""
    pass
```

SimplePyDoc generates:

```markdown
# myproject API Documentation

## Classes

### Class: `Calculator`

A simple calculator.

**Methods:**

- **`add`**: Add two numbers.

## Functions

### `helper()`

A helper function.
```

## Current Scope (MVP)

- ✅ Python files only
- ✅ Parses classes, methods, and functions
- ✅ Extracts docstrings
- ✅ Generates markdown output
- ❌ No template customization (simple, opinionated format)
- ❌ No notebook support
- ❌ No remote repository cloning (use local paths)

## Development

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run the CLI during development
poetry run simplepydoc generate --repo ./src/llm_docgen --output ./docs

# Format code
poetry run black src tests

# Lint
poetry run flake8 src tests
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT - see [LICENSE](LICENSE) for details.
