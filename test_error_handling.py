import unittest

from pychronicle.ast_analyzer import ASTAnalyzer


class TestErrorHandling(unittest.TestCase):

    def test_invalid_python_syntax(self):
        source = "x = "

        with self.assertRaises(SyntaxError):
            ASTAnalyzer(source).analyze()

    def test_empty_source(self):
        source = ""

        statements = ASTAnalyzer(source).analyze()

        self.assertEqual(statements, [])


if __name__ == "__main__":
    unittest.main()