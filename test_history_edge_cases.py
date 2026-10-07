import unittest

from pychronicle.history import History, ExecutionState


class TestHistoryEdgeCases(unittest.TestCase):

    def create_state(self, step):
        return ExecutionState(
            step=step,
            line=step,
            function="<module>",
            source=f"x = {step}",
            variables={"x": step}
        )

    def test_get_invalid_index(self):
        history = History()
        history.add(self.create_state(1))

        self.assertIsNone(history.get(-1))
        self.assertIsNone(history.get(5))

    def test_jump_to_invalid_index(self):
        history = History()
        history.add(self.create_state(1))

        self.assertIsNone(history.jump_to(-1))
        self.assertIsNone(history.jump_to(10))

    def test_empty_history_navigation(self):
        history = History()

        self.assertIsNone(history.get(0))
        self.assertIsNone(history.previous())
        self.assertIsNone(history.next())

    def test_to_dict(self):
        history = History()
        history.add(self.create_state(1))

        result = history.to_dict()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["step"], 1)
        self.assertEqual(result[0]["variables"], {"x": 1})


if __name__ == "__main__":
    unittest.main()