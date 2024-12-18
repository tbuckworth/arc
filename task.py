import numpy as np

from utils import run_prolog_program, prolog2FOL_array, FOL2grid, grid2FOL, FOL2prolog, grid2rgb, \
    plot_grids


class Grid:
    def __init__(self, grid, grid_type):
        self.grid = grid
        self.grid_type = grid_type
        self.preds = grid2FOL(self.grid, self.grid_type)
        self.prolog = FOL2prolog(self.preds)

class Example:
    def __init__(self, example, idx, example_type):
        self.example_type = example_type
        self.i = idx
        self.input_grid = Grid(example["input"], "input")
        self.output_grid = Grid(example["output"], "output")

    def generate_solution(self, solution):
        in_filename = "tmp_input_file"
        with open(f'prolog/{in_filename}.pl', 'w') as file:
            file.write(self.input_grid.prolog)
        program = f"[{in_filename}], [{solution}], [background_knowledge], print_results, halt."
        out_prolog = run_prolog_program(program=program, curr_dir='./prolog')
        if out_prolog is None:
            print(f"Prolog likely timed out.\n"
                  f"Try to run your clauses manually to see whether you get errors "
                  f"or whether you can improve your program's efficiency.")
            return None
        out_FOL_array = prolog2FOL_array(out_prolog)
        return FOL2grid(out_FOL_array)

    def try_solution(self, solution):
        out_grid = self.generate_solution(solution)
        if out_grid is None:
            return False
        same = out_grid == self.output_grid.grid
        result = same.all()
        suffix = "" if result else "in"
        result_txt = f"{same.sum()}/{np.prod(same.shape)}"
        plot_file = self.plot_all(solution, out_grid, result_txt)
        additional_text = "" if result else f"\n\tCheck {plot_file} for more info."
        print(f"Example {self.i}: output {suffix}correct with {result_txt} correct cells.{additional_text}")
        return result

    def plot_all(self, solution, out_grid, result_txt):
        to_plot = [self.input_grid.grid, out_grid, self.output_grid.grid]
        filename = f"plots/{self.example_type}_{solution}_example_{self.i}.png"
        grids = [grid2rgb(x) for x in to_plot]
        plot_grids(grids, filename, result_txt)
        return filename



class Task:
    def __init__(self, task_dict):
        self.task_dict = task_dict
        self.train_examples = [Example(e, i, "Train") for i, e in enumerate(task_dict["train"])]
        self.test_examples = [Example(e, i, "Test") for i, e in enumerate(task_dict["test"])]

    def try_solution(self, solution):
        print("Training Examples:")
        if not self.try_solution_train(solution):
            print("Failed Training")
            return False
        print("Test Examples:")
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
