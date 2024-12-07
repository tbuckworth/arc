import numpy as np

from main import run_prolog_program, prolog2FOL_array, FOL2grid, grid2FOL, FOL2prolog, array_and_plot_grid


class Grid:
    def __init__(self, grid, grid_type):
        self.grid = grid
        self.grid_type = grid_type
        self.preds = grid2FOL(self.grid, self.grid_type)
        self.prolog = FOL2prolog(self.preds)

class Example:
    def __init__(self, example, idx):
        self.i = idx
        self.input_grid = Grid(example["input"], "input")
        self.output_grid = Grid(example["output"], "output")

    def try_solution(self, solution):
        in_filename = "tmp_input_file"
        with open(f'prolog/{in_filename}.pl', 'w') as file:
            file.write(self.input_grid.prolog)
        program = f"[{in_filename}], [{solution}], [background_knowledge], print_results, halt."
        out_prolog = run_prolog_program(program=program, curr_dir='./prolog')

        out_FOL_array = prolog2FOL_array(out_prolog)
        out_grid = FOL2grid(out_FOL_array)
        same = out_grid == self.output_grid.grid
        result = same.all()
        if not result:
            print(f"Example {self.i}: output incorrect due to {(~same).sum()}/{np.prod(same.shape)} cells")
            # array_and_plot_grid(self.input_grid.grid)
            # array_and_plot_grid(out_grid)
            # array_and_plot_grid(self.output_grid.grid)
            # raise Exception
        # TODO: create and save plots
        return result

class Task:
    def __init__(self, task_dict):
        self.task_dict = task_dict
        self.train_examples = [Example(e, i) for i, e in enumerate(task_dict["train"])]
        self.test_examples = [Example(e, i) for i, e in enumerate(task_dict["test"])]

    def try_solution(self, solution):
        if not self.try_solution_train(solution):
            print("Failed Training")
            return False
        if not self.try_solution_test(solution):
            print("Failed Test")
            return False
        return True

    def try_solution_train(self, solution):
        results = [e.try_solution(solution) for e in self.train_examples]
        return np.all(results)

    def try_solution_test(self, solution):
        results = [e.try_solution(solution) for e in self.test_examples]
        return np.all(results)
