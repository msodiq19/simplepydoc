# SimplePyDoc - AI Coding Assistant Instructions

## Project Overview

SimplePyDoc is a Python-based documentation generator that parses Python codebases and generates simple markdown documentation. **MVP Focus**: Python files only, inline markdown generation, no templates.

**Architecture**:

- `src/llm_docgen/parsers/python_parser.py`: AST-based Python code parser
- `src/llm_docgen/cli/commands.py`: Click-based CLI - single entry point
- `docs/repo/`: Sample repository (Ollama Go codebase) for dogfooding/testing

## Development Workflow

### Environment Setup

```bash
# Install dependencies with Poetry
poetry install

# Run tests
poetry run pytest

# Run CLI (MVP - local paths only)
poetry run simplepydoc generate --repo ./src/llm_docgen --output ./docs
```

### Testing Conventions

- Test files in `tests/unit/` follow pattern `test_<module>.py`
- Use pytest fixtures for complex test setup
- CI runs tests across Python 3.8-3.11 (see `.github/workflows/ci.yml`)
- **MVP Tests**: Focus on python_parser.py and end-to-end markdown generation

## Code Patterns & Conventions

### Parser Pattern

All parsers follow AST visitor pattern via `ast.NodeVisitor`:

```python
# Example: parsers/python_parser.py
class CodeAnalyzer(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # Extract metadata with lineno, docstring, args
        self.functions.append({...})
        self.generic_visit(node)  # Always call to traverse children
```

**Key**: Always capture `lineno` for source tracking and use `ast.get_docstring()` for docstrings.

### Markdown Generation (Inline - No Templates)

Generate markdown directly with f-strings:

```python
# Example: Inline markdown generation
def generate_markdown(data: dict) -> str:
    md = f"# {data['project_name']} API\n\n"
    for cls in data['classes']:
        md += f"## Class: {cls['name']}\n{cls['docstring']}\n\n"
    return md
```

**Important**: No Jinja2 templates - keep it simple with string formatting.

### CLI Structure

CLI uses Click groups with the `@cli.command()` decorator pattern:

- Entry point: `cli/commands.py:cli()` (registered in `pyproject.toml`)
- Commands accept `--repo`, `--output` options (no `--template` in MVP)
- Error handling: Use `click.secho(..., fg="red", err=True)` + `raise click.Abort()`

### Repository Processing

When processing repos (see `cli/commands.py:process_repository()`):

1. Accept local path only (no cloning)
2. Walk with `repo_dir.rglob("*.py")` for Python files
3. Parse each file with `CodeAnalyzer` and aggregate results
4. Generate markdown inline with f-strings

## Important Implementation Details

### Error Handling

- Parser: Catch `SyntaxError` and re-raise as `ValueError` with context
- Skip files that fail to parse (log warning, continue processing)

### Path Management

- Always use `Path.mkdir(parents=True, exist_ok=True)` for output directories
- Default output: `./docs/API.md`

## Key Files to Reference

- `src/llm_docgen/cli/commands.py`: Main CLI logic and repo processing flow
- `src/llm_docgen/parsers/python_parser.py`: AST visitor pattern example
- `tests/unit/test_python_parser.py`: Parser testing approach
- `WEEKEND_SPRINT.md`: MVP scope and implementation checklist

## Dependencies & Tools

- **Poetry**: Package manager (no pip/requirements.txt)
- **Click**: CLI framework
- **AST module**: Built-in Python parser (no external dependencies)

## When Adding Features

1. New parsers → Follow `CodeAnalyzer` visitor pattern with `get_result()` method
2. New CLI commands → Add to `cli/commands.py` with `@cli.command()` decorator
3. New dependencies → Add via `poetry add <package>`, commit `pyproject.toml` changes
4. Markdown output → Edit inline generation logic, no templates needed
