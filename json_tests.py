import copy
import unittest

import numpy as np

from main import load_task, grid2FOL, FOL2grid, FOL2prolog, prolog2FOL_array, run_prolog_program, array_and_plot_grid
from task import Task


class TaskTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task_dict = load_task()#"data/training/0b148d64.json")
        cls.task = Task(cls.task_dict)
        # Example of accessing input/output grids for the first example
        cls.input_grid = cls.task_dict['train'][0]['input']
        cls.output_grid = cls.task_dict['train'][0]['output']

        cls.in_preds = grid2FOL(cls.input_grid, "input")
        cls.out_preds = grid2FOL(cls.output_grid, "output")

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

    def test_prolog_program(self):
        in_prolog = FOL2prolog(self.in_preds)
        with open('prolog/input_example_1.pl', 'w') as file:
            file.write(in_prolog)

        program = "[input_example_1], [solution_1], [background_knowledge], print_results, halt."

        out_prolog = run_prolog_program(program=program, curr_dir='./prolog')

        out_FOL_array = prolog2FOL_array(out_prolog)
        out_grid = FOL2grid(out_FOL_array)
        array_and_plot_grid(self.output_grid)
        array_and_plot_grid(out_grid)
        self.assertTrue((out_grid == self.output_grid).all())

    def test_task_class(self):
        solution = "solution_1"
        res = self.task.try_solution(solution)

        print(res)


if __name__ == '__main__':
    unittest.main()
