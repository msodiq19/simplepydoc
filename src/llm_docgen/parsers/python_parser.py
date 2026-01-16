import ast
from typing import Dict, List


def parse_python_code(code: str) -> Dict:
    """Parse python code and extract structured information."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Invalid python code: {e}") from e

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.get_result()


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self._inside_class = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Only add to functions list if not inside a class
        if not self._inside_class:
            docstring = ast.get_docstring(node) or ""
            self.functions.append(
                {
                    "name": node.name,
                    "args": [a.arg for a in node.args.args],
                    "docstring": docstring,
                    "lineno": node.lineno,
                }
            )
            # Continue visiting children for nested definitions
            self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        methods = []

        # Extract methods directly from the class body
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(
                    {"name": item.name, "docstring": ast.get_docstring(item) or ""}
                )

        self.classes.append(
            {
                "name": node.name,
                "docstring": ast.get_docstring(node) or "",
                "methods": methods,
                "lineno": node.lineno,
            }
        )

        # Don't visit children of the class to avoid adding methods to functions
        # (methods are already extracted above)

    def get_result(self) -> Dict:
        return {"functions": self.functions, "classes": self.classes}
