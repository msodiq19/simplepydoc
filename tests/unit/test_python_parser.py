import pytest
from pathlib import Path
from llm_docgen.parsers.python_parser import parse_python_code, CodeAnalyzer
import ast


def test_function_extraction():
    """Test 1: Parse a single Python file with 1 function"""
    code = """\
def add(a: int, b: int) -> int:
    \"\"\"Sum two numbers.\"\"\"
    return a + b
"""
    result = parse_python_code(code)
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "add"
    assert result["functions"][0]["docstring"] == "Sum two numbers."
    assert result["functions"][0]["args"] == ["a", "b"]


def test_class_with_methods():
    """Test 2: Parse a Python file with 1 class + methods"""
    code = """\
class Calculator:
    \"\"\"A simple calculator class.\"\"\"
    
    def add(self, a, b):
        \"\"\"Add two numbers.\"\"\"
        return a + b
    
    def subtract(self, a, b):
        \"\"\"Subtract two numbers.\"\"\"
        return a - b
"""
    result = parse_python_code(code)
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Calculator"
    assert result["classes"][0]["docstring"] == "A simple calculator class."
    assert len(result["classes"][0]["methods"]) == 2
    assert result["classes"][0]["methods"][0]["name"] == "add"
    assert result["classes"][0]["methods"][1]["name"] == "subtract"


def test_multiple_functions_and_classes():
    """Test 3: Parse file with multiple classes and functions"""
    code = """\
def helper():
    \"\"\"A helper function.\"\"\"
    pass

class MyClass:
    \"\"\"First class.\"\"\"
    def method1(self):
        pass

class AnotherClass:
    \"\"\"Second class.\"\"\"
    pass

def another_helper():
    pass
"""
    result = parse_python_code(code)
    assert len(result["functions"]) == 2
    assert len(result["classes"]) == 2
    assert result["functions"][0]["name"] == "helper"
    assert result["classes"][0]["name"] == "MyClass"
    assert result["classes"][1]["name"] == "AnotherClass"


def test_syntax_error_handling():
    """Test 4: Handle file with syntax errors gracefully"""
    code = "def broken syntax here"

    with pytest.raises(ValueError) as exc_info:
        parse_python_code(code)

    assert "Invalid python code" in str(exc_info.value)


def test_no_docstring():
    """Test functions and classes without docstrings"""
    code = """\
def func_no_doc():
    return 42

class ClassNoDoc:
    def method_no_doc(self):
        pass
"""
    result = parse_python_code(code)
    assert result["functions"][0]["docstring"] == ""
    assert result["classes"][0]["docstring"] == ""
    assert result["classes"][0]["methods"][0]["docstring"] == ""


def test_lineno_tracking():
    """Test that line numbers are captured"""
    code = """\
def first():
    pass

class Second:
    pass
"""
    result = parse_python_code(code)
    assert result["functions"][0]["lineno"] == 1
    assert result["classes"][0]["lineno"] == 4
