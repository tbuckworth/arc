import unittest

from main import load_task, tasks
from task import Task


class TaskTester(unittest.TestCase):

    def try_solution(self, task_file, solution):
        print(f"\n{solution}")
        task_dict = load_task(f"secret_tests/{task_file}.json")
        task = Task(task_dict)
        res = task.try_solution(solution)
        self.assertTrue(res)

    def test_solution_2(self):
        self.try_solution("pour", 'solution_2')

    def test_solution_1(self):
        self.try_solution("lines", 'solution_1')

if __name__ == '__main__':
    unittest.main()
