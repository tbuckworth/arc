import numpy as np

from main import colour_lookup, run_prolog_program, prolog2FOL_array, FOL2grid, grid2FOL, FOL2prolog


class Grid:
    def __init__(self, grid, grid_type):
        self.grid = grid
        self.grid_type = grid_type
        self.preds = grid2FOL(self.grid, self.grid_type)
        self.prolog = FOL2prolog(self.preds)

class Example:
    def __init__(self, example):
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
        result = (out_grid == self.output_grid.grid).all()
        return result

class Task:
    def __init__(self, task_dict):
        self.task_dict = task_dict
        self.train_examples = [Example(e) for e in task_dict["train"]]
        self.test_examples = [Example(e) for e in task_dict["test"]]

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
