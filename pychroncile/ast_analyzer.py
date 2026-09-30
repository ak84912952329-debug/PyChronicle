
import ast


class ASTAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code

    def analyze(self):
        tree = ast.parse(self.source_code)

        statements = []

        for node in ast.walk(tree):
            if isinstance(node, ast.stmt):
                statements.append({
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "type": type(node).__name__,
                })

        statements.sort(key=lambda x: x["line"])

        return statements
