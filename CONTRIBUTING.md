# Contributing to SimplePyDoc

Thank you for your interest in contributing to SimplePyDoc! 🎉

## Getting Started

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/msodiq19/simplepydoc.git
cd simplepydoc

# Install dependencies with Poetry
poetry install

# Verify installation
poetry run pytest
```

## Development Workflow

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/unit/test_python_parser.py -v

# Run specific test
poetry run pytest tests/unit/test_cli.py::test_generate_markdown -v
```

### Code Quality

```bash
# Format code with Black
poetry run black src tests

# Lint with flake8
poetry run flake8 src tests

# Run all quality checks
poetry run black src tests && poetry run flake8 src tests && poetry run pytest
```

### Testing Your Changes

```bash
# Test the CLI during development
poetry run simplepydoc generate --repo ./src/llm_docgen --output ./docs

# Test on another project
poetry run simplepydoc generate --repo /path/to/your/project --output ./test-output
```

## Code Conventions

### Parser Pattern

All parsers follow the AST visitor pattern:

```python
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        # Extract function metadata
        self.functions.append({...})
        self.generic_visit(node)  # Continue traversal

    def get_result(self):
        return {"functions": self.functions, "classes": self.classes}
```

**Important**: Always call `generic_visit(node)` to traverse child nodes.

### Error Handling

- Parser: Catch `SyntaxError` and re-raise as `ValueError` with context
- CLI: Use `click.secho(..., fg="red", err=True)` for errors
- Skip unparseable files with warnings, don't abort entire process

### Testing

- Place tests in `tests/unit/test_<module>.py`
- Use descriptive test names: `test_<what>_<scenario>()`
- Add docstrings explaining what each test validates
- Use pytest fixtures for complex setup

Example:

```python
def test_function_extraction():
    """Test parsing a single function with docstring."""
    code = '''
def add(a, b):
    """Add two numbers."""
    return a + b
'''
    result = parse_python_code(code)
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "add"
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Keep changes focused and atomic
- Write tests for new functionality
- Update documentation if needed

### 3. Test Thoroughly

```bash
# Run all tests
poetry run pytest

# Format code
poetry run black src tests

# Check coverage
poetry run pytest --cov=src --cov-report=term-missing
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add support for async functions"
# or
git commit -m "fix: handle empty docstrings correctly"
```

Use conventional commit messages:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 5. Submit a Pull Request

1. Push your branch: `git push origin feature/your-feature-name`
2. Open a PR on GitHub
3. Describe what changed and why
4. Link any related issues

## Project Structure

```
llm-docgen/
├── src/llm_docgen/
│   ├── cli/
│   │   └── commands.py      # CLI entry point
│   └── parsers/
│       └── python_parser.py # AST-based Python parser
├── tests/
│   └── unit/
│       ├── test_cli.py
│       └── test_python_parser.py
├── docs/                    # Generated documentation
├── examples/                # Example outputs
└── pyproject.toml          # Poetry configuration
```

## Adding Features

### New Parser Functionality

When extending the Python parser:

1. Update `CodeAnalyzer` visitor class
2. Add extraction logic in appropriate `visit_*` method
3. Update `get_result()` to include new data
4. Add tests in `test_python_parser.py`
5. Update markdown generator in `commands.py`

### New CLI Options

When adding CLI options:

1. Add `@click.option()` to `generate()` command
2. Update function signature
3. Implement the feature
4. Add tests in `test_cli.py`
5. Update README with examples

## Scope & Vision

SimplePyDoc is intentionally **simple and focused**:

✅ **In Scope**:

- Python code parsing (classes, functions, docstrings)
- Markdown output generation
- Local directory processing
- CLI interface

❌ **Out of Scope** (for MVP):

- Template customization
- Multiple output formats (HTML, PDF, etc.)
- Remote repository cloning
- Jupyter notebook parsing
- Other languages beyond Python

If proposing a feature, consider:

- Does it align with the "simple Python docs" mission?
- Can it be implemented without heavy dependencies?
- Will it complicate the user experience?

## Questions?

- Open an issue for discussion
- Check existing issues and PRs
- Review `WEEKEND_SPRINT.md` for project goals

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to learn and build something useful together.

---

Thank you for contributing! 🚀
