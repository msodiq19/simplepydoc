# LLM DocGen 🚀

[![CI](https://github.com/msodiq19/llm-docgen/actions/workflows/ci.yml/badge.svg)](https://github.com/msodiq19/llm-docgen/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Development Status](https://img.shields.io/badge/status-early%20development-orange.svg)]()

Automatically generate documentation for Python projects, with a focus on Large Language Model (LLM) and Machine Learning codebases.

## ⚠️ Project Status

**EARLY DEVELOPMENT - NOT PRODUCTION READY**

This project is currently in early development (v0.1.0). Core functionality is partially implemented but not yet fully working. See [PROJECT_COMPLETION_PLAN.md](PROJECT_COMPLETION_PLAN.md) for detailed status and roadmap.

**What works:**
- ✅ Basic Python code parsing (classes, functions, docstrings)
- ✅ Template system foundation (Jinja2)
- ✅ CLI structure (Click-based)
- ✅ Basic test infrastructure

**What's missing/broken:**
- ❌ Default template not fully implemented
- ❌ Notebook parsing incomplete
- ❌ No configuration file support
- ❌ Not installable via pip yet
- ❌ Limited error handling
- ❌ No comprehensive documentation

**Completion estimate:** 40-60 hours of development work needed for MVP.

See [REQUIREMENTS.md](REQUIREMENTS.md) for detailed requirements and [ARCHITECTURE.md](ARCHITECTURE.md) for technical design.

## Planned Features

When complete, LLM DocGen will:
- 📚 Parse Python codebases and extract structured information
- 🔍 Extract usage examples from Jupyter notebooks
- 🎨 Generate documentation using customizable templates
- 🚀 Provide a simple CLI interface
- 📊 Support both Markdown and HTML output
- ⚙️ Allow configuration via YAML files

Future extensions may include:
- Multi-language support (JavaScript, Go, etc.)
- LLM-specific features (model cards, training configs)
- GitHub Actions integration
- IDE plugins

## Quick Start (For Developers)

**Note:** The tool is not yet publishable to PyPI. Install from source for development.

### Installation

```bash
# Clone the repository
git clone https://github.com/msodiq19/llm-docgen.git
cd llm-docgen

# Install with Poetry
poetry install

# Or install with pip in development mode
pip install -e .
```

### Basic Usage

```bash
# Generate documentation for a local Python project
poetry run llm-docgen generate --repo /path/to/project --output ./docs

# Or if installed with pip
llm-docgen generate --repo /path/to/project --output ./docs
