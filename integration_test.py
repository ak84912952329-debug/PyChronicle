import unittest

from pychronicle.ast_analyzer import ASTAnalyzer
from pychronicle.history import History
from pychronicle.tracer import ExecutionTracer


class TestPyChronicleIntegration(unittest.TestCase):

    def test_ast_and_tracer_integration(self):
        source_code = """x = 10
y = 20
z = x + y
"""

        # Step 1: Analyze the source code using AST
        analyzer = ASTAnalyzer(source_code)
        statements = analyzer.analyze()

        self.assertEqual(len(statements), 3)

        # Step 2: Trace execution of the same source code
        tracer = ExecutionTracer()

        compiled_code = compile(
            source_code,
            "<integration_test>",
            "exec"
        )

        namespace = {}

        tracer.start()
        try:
            exec(compiled_code, namespace)
        finally:
            tracer.stop()

        # Step 3: Check that execution states were recorded
        self.assertGreater(len(tracer.history), 0)

        # Step 4: Store traced states in History
        history = History()

        for state in tracer.history:
            history.add(state)

        # Step 5: Verify history
        self.assertGreater(len(history), 0)
        self.assertIsNotNone(history.get(0))

        # Verify the final result
        self.assertEqual(namespace["z"], 30)


if __name__ == "__main__":
    unittest.main()