#  API Documentation

## Classes

### Class: `CodeAnalyzer`

**Methods:**

- **`__init__`**
- **`visit_FunctionDef`**
- **`visit_ClassDef`**
- **`get_result`**

## Functions

### `test_function_extraction()`

Test 1: Parse a single Python file with 1 function

### `test_class_with_methods()`

Test 2: Parse a Python file with 1 class + methods

### `test_multiple_functions_and_classes()`

Test 3: Parse file with multiple classes and functions

### `test_syntax_error_handling()`

Test 4: Handle file with syntax errors gracefully

### `test_no_docstring()`

Test functions and classes without docstrings

### `test_lineno_tracking()`

Test that line numbers are captured

### `test_generate_markdown()`

Test markdown generation from parsed data

### `test_process_repository()`

Test processing a directory of Python files

### `test_cli_generate_command()`

Test the CLI generate command end-to-end

### `test_cli_nonexistent_repo()`

Test CLI with nonexistent repository path

### `generate_markdown(data)`

Generate markdown documentation from parsed code data.

### `cli()`

LLM Documentation Generator

### `generate(repo, output)`

Generate documentation from a repository

### `process_repository(repo_dir)`

Process the repository to extract documentation data.

### `parse_python_code(code)`

Parse python code and extract structured information.

