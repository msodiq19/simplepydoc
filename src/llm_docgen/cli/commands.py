import click
from pathlib import Path
import ast
from llm_docgen.parsers.python_parser import CodeAnalyzer


def generate_markdown(data: dict) -> str:
    """Generate markdown documentation from parsed code data."""
    md = f"# {data['project_name']} API Documentation\n\n"

    if data["classes"]:
        md += "## Classes\n\n"
        for cls in data["classes"]:
            md += f"### Class: `{cls['name']}`\n\n"
            if cls["docstring"]:
                md += f"{cls['docstring']}\n\n"

            if cls["methods"]:
                md += "**Methods:**\n\n"
                for method in cls["methods"]:
                    md += f"- **`{method['name']}`**"
                    if method["docstring"]:
                        md += f": {method['docstring']}"
                    md += "\n"
                md += "\n"

    if data["functions"]:
        md += "## Functions\n\n"
        for func in data["functions"]:
            args_str = ", ".join(func["args"])
            md += f"### `{func['name']}({args_str})`\n\n"
            if func["docstring"]:
                md += f"{func['docstring']}\n\n"

    return md


@click.group()
def cli():
    """LLM Documentation Generator"""


@cli.command()
@click.option("--repo", required=True, help="Local path to repository")
@click.option("--output", default="docs", help="Output directory")
def generate(repo: str, output: str):
    """Generate documentation from a repository"""
    try:
        repo_dir = Path(repo)
        if not repo_dir.exists():
            click.secho(
                f"Error: Repository path '{repo}' does not exist", fg="red", err=True
            )
            raise click.Abort()

        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        click.echo(f"Processing repository: {repo_dir}")

        # Process the repository to generate documentation
        documentation_data = process_repository(repo_dir)

        # Generate markdown documentation
        rendered_docs = generate_markdown(documentation_data)

        # Save the rendered documentation to the output directory
        output_file = output_path / "API.md"
        with open(output_file, "w") as f:
            f.write(rendered_docs)

        click.secho(f"✓ Successfully generated docs: {output_file}", fg="green")

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)
        raise click.Abort()


def process_repository(repo_dir: Path) -> dict:
    """Process the repository to extract documentation data."""
    documentation_data = {"project_name": repo_dir.name, "classes": [], "functions": []}

    # Iterate through Python files in the repository
    python_files = list(repo_dir.rglob("*.py"))
    click.echo(f"Found {len(python_files)} Python files")

    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()
                # Use CodeAnalyzer to parse the code
                analyzer = CodeAnalyzer()
                tree = ast.parse(code)
                analyzer.visit(tree)
                documentation_data["classes"].extend(analyzer.classes)
                documentation_data["functions"].extend(analyzer.functions)
        except SyntaxError as e:
            click.secho(f"  ⚠ Skipping {py_file.name}: {e}", fg="yellow")
        except Exception as e:
            click.secho(f"  ⚠ Error processing {py_file.name}: {e}", fg="yellow")

    # Summary
    click.echo(
        f"Extracted {len(documentation_data['classes'])} classes, {len(documentation_data['functions'])} functions"
    )

    return documentation_data
