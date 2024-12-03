import copy
import unittest

import numpy as np

from main import load_task, FOL2grid, FOL2prolog, prolog2FOL_array, tasks
from task import Task


class TaskTester(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.task_dict = load_task("data/training/d4f3cd78.json")
    #     cls.task = Task(cls.task_dict)
    #     # Example of accessing input/output grids for the first example
    #     cls.output_grid = cls.task.train_examples[0].output_grid.grid
    #     cls.out_preds = cls.task.train_examples[0].output_grid.preds


    def try_solution(self, task_file, solution):
        task_dict = load_task(f"data/training/{task_file}")
        task = Task(task_dict)
        res = task.try_solution(solution)
        self.assertTrue(res)

    def test_solution_1(self):
        self.try_solution(tasks["lines"], 'solution_1')

    def test_solution_2(self):
        self.try_solution(tasks["pour"], 'solution_2')

if __name__ == '__main__':
    unittest.main()
