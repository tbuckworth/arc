import copy
import unittest

import numpy as np

from main import load_task, grid2FOL, FOL2grid, FOL2prolog, prolog2FOL_array, run_prolog_program


class TaskTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = load_task()#"data/training/0b148d64.json")
        # Example of accessing input/output grids for the first example
        cls.input_grid = cls.task['train'][0]['input']
        cls.output_grid = cls.task['train'][0]['output']

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
        # with open('prolog/solution_1.pl', 'rt') as file:
        #     prolog_program = file.read()

        # full_program = in_prolog + prolog_program
        #
        # with open('prolog/temp.pl', 'w') as file:
        #     file.write(full_program)

        program = """
        working_directory(prolog).
        compile(input_example_1).
        compile(solution_1).
        write('done!'), nl, halt.
        """
        # output_colour(R, C, Colour).

        out = run_prolog_program(program)

        print(out)




if __name__ == '__main__':
    unittest.main()
