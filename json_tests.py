import copy
import unittest

import numpy as np

from main import load_task, FOL2grid, FOL2prolog, prolog2FOL_array
from task import Task


class TaskTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task_dict = load_task("data/training/d4f3cd78.json")
        cls.task = Task(cls.task_dict)
        # Example of accessing input/output grids for the first example
        cls.output_grid = cls.task.train_examples[0].output_grid.grid
        cls.out_preds = cls.task.train_examples[0].output_grid.preds

    def test_ordering(self):
        out_preds = copy.deepcopy(self.out_preds)
        np.random.shuffle(out_preds)
        [np.random.shuffle(x) for x in out_preds]
        self.assertTrue((self.output_grid == FOL2grid(out_preds)).all())

    def test_print(self):
        out_prolog = FOL2prolog(self.out_preds)
        out_FOL_array = prolog2FOL_array(out_prolog)
        out_grid = FOL2grid(out_FOL_array)
        self.assertTrue((out_grid == self.output_grid).all())

    def test_task_class(self):
        solution = "solution_2"
        res = self.task.try_solution(solution)
        self.assertTrue(res)

    def test_task_empty(self):
        res = self.task.try_solution("empty_solution")
        self.assertFalse(res)

if __name__ == '__main__':
    unittest.main()
