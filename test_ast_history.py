import unittest

from pychronicle.ast_analyzer import ASTAnalyzer
from pychronicle.history import History, ExecutionState


class TestASTAnalyzerExtended(unittest.TestCase):

    def test_statement_details(self):
        source = """x = 10
y = 20
z = x + y
print(z)
"""

        analyzer = ASTAnalyzer(source)
        statements = analyzer.analyze()

        self.assertEqual(len(statements), 4)

        self.assertEqual(statements[0]["line"], 1)
        self.assertEqual(statements[0]["type"], "Assign")

        self.assertEqual(statements[1]["line"], 2)
        self.assertEqual(statements[1]["type"], "Assign")

        self.assertEqual(statements[2]["line"], 3)
        self.assertEqual(statements[2]["type"], "Assign")

        self.assertEqual(statements[3]["line"], 4)
        self.assertEqual(statements[3]["type"], "Expr")


class TestHistoryExtended(unittest.TestCase):

    def create_history(self):
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

        return history

    def test_history_length(self):
        history = self.create_history()

        self.assertEqual(len(history), 3)

    def test_invalid_indexes(self):
        history = self.create_history()

        self.assertIsNone(history.get(-1))
        self.assertIsNone(history.get(10))

        self.assertIsNone(history.jump_to(10))

    def test_jump_and_navigation(self):
        history = self.create_history()

        self.assertEqual(history.jump_to(1).step, 2)
        self.assertEqual(history.previous().step, 1)
        self.assertEqual(history.next().step, 2)
        self.assertEqual(history.next().step, 3)

    def test_to_dict(self):
        history = self.create_history()

        data = history.to_dict()

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["step"], 1)
        self.assertEqual(data[0]["variables"], {"x": 0})


if __name__ == "__main__":
    unittest.main()