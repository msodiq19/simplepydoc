import pytest
from pathlib import Path
from click.testing import CliRunner
from llm_docgen.cli.commands import cli, generate_markdown, process_repository
import tempfile
import shutil


def test_generate_markdown():
    """Test markdown generation from parsed data"""
    data = {
        "project_name": "TestProject",
        "classes": [
            {
                "name": "MyClass",
                "docstring": "A test class.",
                "methods": [
                    {"name": "method1", "docstring": "First method"},
                    {"name": "method2", "docstring": ""},
                ],
            }
        ],
        "functions": [
            {
                "name": "my_function",
                "args": ["arg1", "arg2"],
                "docstring": "A test function.",
            }
        ],
    }

    result = generate_markdown(data)

    assert "# TestProject API Documentation" in result
    assert "## Classes" in result
    assert "### Class: `MyClass`" in result
    assert "A test class." in result
    assert "**`method1`**" in result
    assert "## Functions" in result
    assert "`my_function(arg1, arg2)`" in result
    assert "A test function." in result


def test_process_repository():
    """Test processing a directory of Python files"""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test_repo"
        test_dir.mkdir()

        # Create test Python file
        test_file = test_dir / "module.py"
        test_file.write_text(
            """
def hello():
    \"\"\"Say hello.\"\"\"
    return "Hello"

class Greeter:
    \"\"\"A greeter class.\"\"\"
    def greet(self):
        \"\"\"Greet someone.\"\"\"
        pass
"""
        )

        result = process_repository(test_dir)

        assert result["project_name"] == "test_repo"
        assert len(result["functions"]) == 1
        assert len(result["classes"]) == 1
        assert result["functions"][0]["name"] == "hello"
        assert result["classes"][0]["name"] == "Greeter"


def test_cli_generate_command():
    """Test the CLI generate command end-to-end"""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test repository
        repo_dir = Path(tmpdir) / "repo"
        repo_dir.mkdir()

        test_file = repo_dir / "test.py"
        test_file.write_text(
            """
def sample():
    \"\"\"A sample function.\"\"\"
    pass
"""
        )

        # Create output directory
        output_dir = Path(tmpdir) / "output"

        # Run CLI command
        result = runner.invoke(
            cli, ["generate", "--repo", str(repo_dir), "--output", str(output_dir)]
        )

        assert result.exit_code == 0
        assert "Successfully generated docs" in result.output

        # Check output file exists
        output_file = output_dir / "API.md"
        assert output_file.exists()

        # Check content
        content = output_file.read_text()
        assert "repo API Documentation" in content
        assert "sample" in content


def test_cli_nonexistent_repo():
    """Test CLI with nonexistent repository path"""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate", "--repo", "/nonexistent/path"])

    assert result.exit_code == 1
    assert "does not exist" in result.output
