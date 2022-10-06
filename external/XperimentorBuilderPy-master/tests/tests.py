import unittest

from main import get_cartesian_prod


class TestFunctions(unittest.TestCase):
    def test_get_cartesian_prod(self):
        process = {
            'id': 'Test',
            'command': 'This {is} a single {test} {case}'
        }

        usages = {
            'is': [-1],
            'test': ['c', 1.0],
            'case': [1, 2, 3],
        }

        expected = [
            [-1, 'c', 1],
            [-1, 'c', 2],
            [-1, 'c', 3],

            [-1, 1.0, 1],
            [-1, 1.0, 2],
            [-1, 1.0, 3],
        ]

        actual = get_cartesian_prod(process, usages)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
