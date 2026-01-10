# Contributing to LLM DocGen

Thank you for your interest in contributing to LLM DocGen! This document provides guidelines and information for contributors.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Areas Where Help is Needed](#areas-where-help-is-needed)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or identity.

### Our Standards
- Be respectful and constructive
- Accept feedback graciously
- Focus on what's best for the project
- Show empathy towards others

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Poetry (recommended) or pip

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/llm-docgen.git
cd llm-docgen

# Install dependencies
poetry install

# Run tests to verify setup
poetry run pytest
```

## Development Workflow

1. **Pick an Issue** - Check GitHub Issues for open tasks
2. **Create Branch** - `git checkout -b feature/your-feature`
3. **Write Code** - Follow coding standards
4. **Write Tests** - Test your changes
5. **Commit** - Use clear commit messages
6. **Push & PR** - Create pull request

## Coding Standards

- Follow PEP 8 (88 char line length)
- Add type hints to all functions
- Write docstrings (Google style)
- Keep functions small and focused

## Testing Guidelines

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=llm_docgen
```

- Aim for 80%+ coverage
- Test edge cases and errors
- Use descriptive test names

## Pull Request Process

- Ensure tests pass
- Update documentation
- Reference related issues
- Request review from maintainers

## Areas Where Help is Needed

### High Priority
1. Fix default template implementation
2. Complete Python parser (decorators, type hints)
3. Fix notebook parser
4. Add error handling
5. Increase test coverage

### Medium Priority
6. Configuration file support
7. Progress indicators
8. User documentation
9. CLI improvements
10. Performance optimization

See [PROJECT_COMPLETION_PLAN.md](PROJECT_COMPLETION_PLAN.md) for more details.

---

Thank you for contributing! 🙏
