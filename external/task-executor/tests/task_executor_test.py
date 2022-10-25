import unittest

from task_executor import execute_task


class TaskExecutorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_execute_task(self):
        self.assertEqual({
            "return_code": 0,
            "stderr": "1\n3\n",
            "stdout": "0\n2\n"
        }, execute_task("python error_test.py"))

        self.assertEqual({
            "return_code": 0,
            "stderr": "",
            "stdout": "Hello World!\n"
        }, execute_task("echo Hello World!"))


if __name__ == '__main__':
    unittest.main()
