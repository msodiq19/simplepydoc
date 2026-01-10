# Quickstart Guide - LLM DocGen

## Introduction

This guide will help you get started with LLM DocGen quickly. By the end of this guide, you'll have generated documentation for a Python project.

**Note:** This project is in early development. Some features mentioned may not be fully implemented yet.

## Prerequisites

Before you begin, ensure you have:
- Python 3.9 or higher installed
- Git installed
- Basic familiarity with command line

## Installation

### For Development (Current Recommended Method)

Since the project is not yet published to PyPI, install from source:

```bash
# Clone the repository
git clone https://github.com/msodiq19/llm-docgen.git
cd llm-docgen

# Install with Poetry (recommended)
poetry install

# Verify installation
poetry run llm-docgen --help
```

### For End Users (Future)

Once published to PyPI, you'll be able to install with:

```bash
pip install llm-docgen
```

## Your First Documentation

Let's generate documentation for a sample Python project.

### Step 1: Create a Sample Project

Create a simple Python project to test with:

```bash
# Create a new directory for testing
mkdir ~/test-llm-docgen
cd ~/test-llm-docgen

# Create a sample Python file
cat > calculator.py << 'EOF'
"""A simple calculator module."""

class Calculator:
    """A calculator for basic arithmetic operations."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The sum of a and b
        """
        return a + b
    
    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a.
        
        Args:
            a: Number to subtract from
            b: Number to subtract
            
        Returns:
            The difference of a and b
        """
        return a - b

def multiply(x: float, y: float) -> float:
    """Multiply two numbers.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        The product of x and y
    """
    return x * y
EOF
```

### Step 2: Generate Documentation

Navigate back to the llm-docgen directory and run:

```bash
cd /path/to/llm-docgen

# Generate documentation for the test project
poetry run llm-docgen generate --repo ~/test-llm-docgen --output ~/test-llm-docgen/docs
```

**Expected Output:**
```
Cloning repository from ~/test-llm-docgen...
Repository cloned successfully.
Processing file: /path/to/calculator.py
Successfully generated docs in ~/test-llm-docgen/docs
```

### Step 3: View the Generated Documentation

```bash
# View the generated documentation
cat ~/test-llm-docgen/docs/default.md
```

You should see structured documentation of your Calculator class and multiply function.

## Common Use Cases

### Documenting a Local Project

```bash
llm-docgen generate --repo /path/to/your/project --output ./docs
```

### Using a Custom Template (When Implemented)

```bash
llm-docgen generate --repo /path/to/project --template api-reference
```

### Specifying Output Directory

```bash
llm-docgen generate --repo /path/to/project --output /path/to/docs
```

## Understanding the Output

The generated documentation includes:

1. **Project Name** - Extracted from the directory name
2. **Classes** - All classes found in Python files
   - Class docstrings
   - Methods with their signatures and docstrings
3. **Functions** - Module-level functions
   - Function signatures
   - Parameter types
   - Return types
   - Docstrings

## Customizing Templates

*(Coming in future versions)*

You'll be able to customize the output by:
1. Creating custom Jinja2 templates
2. Placing them in `.llmdocgen/templates/`
3. Referencing them with `--template` flag

## Configuration File

*(Coming in future versions)*

Create a `.llmdocgen.yaml` file in your project root:

```yaml
project:
  name: "My Project"
  version: "1.0.0"

output:
  directory: "docs"
  template: "default"

parsing:
  exclude:
    - "tests/*"
    - "*.pyc"
  include_private: false
```

## Troubleshooting

### Issue: "Template default not found"

**Cause:** Default template is not fully implemented yet  
**Solution:** This is a known issue. Check [GitHub Issues](https://github.com/msodiq19/llm-docgen/issues) for updates

### Issue: "ModuleNotFoundError: No module named 'llm_docgen'"

**Cause:** Package not installed correctly  
**Solution:** 
```bash
cd /path/to/llm-docgen
poetry install
```

### Issue: "No classes or functions detected"

**Cause:** Files might be excluded or have no docstrings  
**Solution:** 
- Ensure Python files have valid syntax
- Check that files are not in excluded directories
- Add docstrings to your classes and functions

### Issue: Command runs but produces no output

**Cause:** Output directory might not be created or template rendering failed  
**Solution:**
- Check that output directory exists
- Run with `--verbose` flag (when implemented)
- Check for error messages in console

## Next Steps

Now that you've generated your first documentation:

1. **Explore Templates** - Try different built-in templates (when available)
2. **Add Notebooks** - Include Jupyter notebooks with examples
3. **Customize Output** - Create your own templates
4. **Automate** - Set up CI/CD to auto-generate docs

## Getting Help

- **Documentation:** Check [README.md](README.md) and other docs
- **Issues:** Report bugs or request features on [GitHub Issues](https://github.com/msodiq19/llm-docgen/issues)
- **Questions:** Open a discussion on GitHub

## Examples

### Example 1: Documenting an ML Project

```bash
# Clone an ML project
git clone https://github.com/example/ml-project.git
cd ml-project

# Generate docs
llm-docgen generate --repo . --output ./docs --template default
```

### Example 2: Including Notebook Examples

*(Coming soon - not yet implemented)*

```bash
# Project structure:
# my-project/
#   ├── src/
#   │   └── model.py
#   └── notebooks/
#       └── usage_example.ipynb

llm-docgen generate --repo my-project --template examples
```

This will extract code examples from notebooks and include them in the documentation.

## What's Next?

- **Read the Requirements:** [REQUIREMENTS.md](REQUIREMENTS.md)
- **Understand the Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Track Progress:** [PROJECT_COMPLETION_PLAN.md](PROJECT_COMPLETION_PLAN.md)

---

**Happy documenting!** 📚
