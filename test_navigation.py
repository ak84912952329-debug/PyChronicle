import unittest

from pychronicle.history import History, ExecutionState
from navigation import Navigation


class TestNavigation(unittest.TestCase):

    def create_navigation(self):
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

        return Navigation(history)

    def test_current(self):
        navigation = self.create_navigation()

        self.assertIsNone(navigation.current())

        navigation.jump_to(0)

        self.assertEqual(navigation.current().step, 1)

    def test_next(self):
        navigation = self.create_navigation()

        navigation.jump_to(0)

        self.assertEqual(navigation.next().step, 2)
        self.assertEqual(navigation.next().step, 3)

    def test_previous(self):
        navigation = self.create_navigation()

        navigation.jump_to(2)

        self.assertEqual(navigation.previous().step, 2)
        self.assertEqual(navigation.previous().step, 1)

    def test_jump_to(self):
        navigation = self.create_navigation()

        self.assertEqual(navigation.jump_to(1).step, 2)
        self.assertEqual(navigation.current().step, 2)

    def test_invalid_jump(self):
        navigation = self.create_navigation()

        self.assertIsNone(navigation.jump_to(10))
        self.assertIsNone(navigation.jump_to(-1))


if __name__ == "__main__":
    unittest.main()