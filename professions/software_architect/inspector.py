"""
Marcus Sterling's Software Architecture Inspector
Deep empirical AST-based measurement engine for modularity, cyclomatic complexity,
silent error suppression, and type contract completeness.
"""

import os
import ast
import re
from typing import Dict, Any, List, Optional, Tuple


class ComplexityVisitor(ast.NodeVisitor):
    """Calculates McCabe Cyclomatic Complexity for Python functions."""

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.complexity += len(node.generators)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.complexity += len(node.generators)
        self.generic_visit(node)


class MarcusArchitectureInspector:
    """Marcus Sterling's Code Architecture & Systems Inspection Engine."""

    def __init__(self, target_file: str):
        self.target_file = os.path.abspath(target_file)

    def inspect(self) -> Dict[str, Any]:
        """
        Executes an objective, deep architectural inspection:
        - Max & average cyclomatic complexity
        - Max function line length & God function detection (>50 lines)
        - Silent exception suppression (unhandled pass in except block)
        - Stubs, placeholders, and unfinished tasks
        - Type annotations percentage on functions
        """
        metrics: Dict[str, Any] = {
            "target": self.target_file,
            "file_type": "unknown",
            "total_lines": 0,
            "functions_count": 0,
            "max_cyclomatic_complexity": 1,
            "avg_cyclomatic_complexity": 1.0,
            "max_function_lines": 0,
            "god_functions_count": 0,
            "silent_exception_swallows": 0,
            "todo_placeholder_count": 0,
            "type_annotation_pct": 100.0,
            "has_global_mutation": False
        }

        if not os.path.exists(self.target_file):
            metrics["error"] = f"File {self.target_file} does not exist"
            return metrics

        ext = os.path.splitext(self.target_file)[1].lower()

        try:
            with open(self.target_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            metrics["total_lines"] = len(content.splitlines())
            metrics["todo_placeholder_count"] = len(re.findall(r"\b(?:TODO|FIXME|HACK|XXX)\b", content, re.IGNORECASE))

            if ext == ".py":
                metrics["file_type"] = "python"
                self._inspect_python_ast(content, metrics)
            elif ext in (".js", ".ts", ".jsx", ".tsx"):
                metrics["file_type"] = "javascript_typescript"
                self._inspect_javascript(content, metrics)
            else:
                metrics["file_type"] = "generic_code"
                self._inspect_generic(content, metrics)

        except Exception as e:
            metrics["inspection_error"] = str(e)

        return metrics

    def _inspect_python_ast(self, content: str, metrics: Dict[str, Any]):
        """Inspects Python source code using AST node traversal."""
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            metrics["syntax_error"] = str(e)
            return

        complexities: List[int] = []
        function_lengths: List[int] = []
        typed_functions = 0
        total_functions = 0
        silent_catches = 0
        has_global = False

        for node in ast.walk(tree):
            # Check for global mutations
            if isinstance(node, ast.Global):
                has_global = True

            # Check for silent exception swallows (except ...: pass)
            if isinstance(node, ast.ExceptHandler):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    silent_catches += 1

            # Check functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_functions += 1

                # Calculate lines
                end_lineno = getattr(node, "end_lineno", node.lineno)
                fn_len = (end_lineno - node.lineno) + 1
                function_lengths.append(fn_len)

                # Calculate cyclomatic complexity
                cv = ComplexityVisitor()
                for child in node.body:
                    cv.visit(child)
                complexities.append(cv.complexity)

                # Check type annotations (returns and args)
                has_return_type = (node.returns is not None)
                args_typed = all(arg.annotation is not None for arg in node.args.args if arg.arg != "self" and arg.arg != "cls")
                if has_return_type or args_typed:
                    typed_functions += 1

        metrics["functions_count"] = total_functions
        metrics["silent_exception_swallows"] = silent_catches
        metrics["has_global_mutation"] = has_global

        if complexities:
            metrics["max_cyclomatic_complexity"] = max(complexities)
            metrics["avg_cyclomatic_complexity"] = round(sum(complexities) / len(complexities), 1)

        if function_lengths:
            metrics["max_function_lines"] = max(function_lengths)
            metrics["god_functions_count"] = sum(1 for fl in function_lengths if fl > 50)

        if total_functions > 0:
            metrics["type_annotation_pct"] = round((typed_functions / total_functions) * 100, 1)

    def _inspect_javascript(self, content: str, metrics: Dict[str, Any]):
        """Inspects JavaScript / TypeScript source code."""
        empty_catches = len(re.findall(r"catch\s*\([^)]*\)\s*\{\s*\}", content))
        metrics["silent_exception_swallows"] = empty_catches

        # Functions
        fn_matches = re.findall(r"(?:function\s+\w+|\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", content)
        metrics["functions_count"] = len(fn_matches)

        # Branching keyword complexity
        branches = len(re.findall(r"\b(if|else if|while|for|switch|case|catch)\b|\?.*:", content))
        metrics["max_cyclomatic_complexity"] = max(1, round(branches / max(1, len(fn_matches))))

        has_types = bool(re.search(r":\s*(?:string|number|boolean|any|void|\w+\[\])", content))
        metrics["type_annotation_pct"] = 100.0 if has_types else 0.0

    def _inspect_generic(self, content: str, metrics: Dict[str, Any]):
        """Fallback for generic source text."""
        lines = content.splitlines()
        metrics["max_function_lines"] = len(lines)
