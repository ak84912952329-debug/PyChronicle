import unittest

from pychronicle.ast_analyzer import ASTAnalyzer
from pychronicle.history import History, ExecutionState
from pychronicle.tracer import ExecutionTracer


class TestASTAnalyzer(unittest.TestCase):

    def test_ast_analysis(self):
        source = """x = 10
y = 20
z = x + y
"""

        analyzer = ASTAnalyzer(source)
        statements = analyzer.analyze()

        self.assertEqual(len(statements), 3)
        self.assertEqual(statements[0]["type"], "Assign")


class TestHistory(unittest.TestCase):

    def test_add_and_get(self):
        history = History()

        state = ExecutionState(
            step=1,
            line=1,
            function="<module>",
            source="x = 10",
            variables={"x": 10}
        )

        history.add(state)

        self.assertEqual(len(history), 1)
        self.assertEqual(history.get(0), state)

    def test_navigation(self):
        history = History()

        for i in range(3):
            state = ExecutionState(
                step=i + 1,
                line=i + 1,
                function="<module>",
                source=f"x = {i}",
                variables={"x": i}
            )
            history.add(state)

        self.assertEqual(history.jump_to(0).step, 1)
        self.assertEqual(history.next().step, 2)
        self.assertEqual(history.next().step, 3)
        self.assertEqual(history.previous().step, 2)


class TestExecutionTracer(unittest.TestCase):

    def test_tracing(self):
        tracer = ExecutionTracer()

        tracer.start()

        x = 10
        y = 20
        z = x + y

        tracer.stop()

        self.assertGreater(len(tracer.history), 0)


if __name__ == "__main__":
    unittest.main()