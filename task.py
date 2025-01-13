import os
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
    def __init__(self, example, idx, example_type, task_name):
        self.task_name = task_name
        self.example_type = example_type
        self.i = idx
        self.input_grid = Grid(example["input"], "input")
        self.output_grid = Grid(example["output"], "output")

    def generate_solution(self, solution):
        prolog_dir = "prolog"
        if not os.path.exists(prolog_dir):
            prolog_dir = "../provided/prolog"
        in_filename = "tmp_input_file"
        with open(f'{prolog_dir}/{in_filename}.pl', 'w') as file:
            file.write(self.input_grid.prolog)
        program = f"[{in_filename}], [helpers], [{solution}], [background_knowledge], print_results, halt."
        out_prolog = run_prolog_program(program=program, curr_dir=prolog_dir)
        if out_prolog is None:
            print(f"Prolog likely timed out.\n"
                  f"Try to run your clauses manually to see whether you get errors "
                  f"or whether you can improve your program's efficiency.")
            return None
        try:
            out_FOL_array = prolog2FOL_array(out_prolog)
            return FOL2grid(out_FOL_array)
        except Exception:
            print("Error in processing solution. Try running prolog locally.")
            print(out_prolog)
            return None

    def try_solution(self, solution, results_info):
        out_grid = self.generate_solution(solution)
        name = f"{self.task_name} - {self.example_type} Example {self.i}"
        if out_grid is None:
            results_info.append({"score":0,
                                 "name":name,
                                 "possible":np.prod(np.array(self.output_grid.grid).shape).item()})
            return False
        same = out_grid == self.output_grid.grid
        result = same.all()
        suffix = "" if result else "in"
        result_txt = f"{same.sum()}/{np.prod(same.shape)}"
        plot_file = self.plot_all(solution, out_grid, result_txt)
        additional_text = ""# if result else f"\n\tCheck {plot_file} for more info."
        print(f"Example {self.i}: output {suffix}correct with {result_txt} correct cells.{additional_text}")
        results_info.append({"score":same.sum().item(),
                             "name":name,
                             "possible":np.prod(same.shape).item()})
        return result

    def plot_all(self, solution, out_grid, result_txt):
        to_plot = [self.input_grid.grid, out_grid, self.output_grid.grid]
        if not os.path.exists("plots"):
            os.mkdir("plots")
        filename = f"plots/{self.example_type}_{solution}_example_{self.i}.pdf"
        #TODO REMOVE THIS!
        # print(np.array(self.input_grid.grid))
        grids = [grid2rgb(x) for x in to_plot]
        # print(np.array(grids[0]))
        #correct up until here
        plot_grids(grids, filename, result_txt)
        return filename


class Task:
    def __init__(self, task_dict, name):
        self.name = name
        self.task_dict = task_dict
        self.train_examples = [Example(e, i, "Train", self.name) for i, e in enumerate(task_dict["train"])]
        self.test_examples = [Example(e, i, "Test", self.name) for i, e in enumerate(task_dict["test"])]

    def try_solution(self, solution, results_info):
        print("Training Examples:")
        success = True
        if not self.try_solution_train(solution, results_info):
            print("Failed Training")
            success = False
        print("Test Examples:")
        if not self.try_solution_test(solution, results_info):
            print("Failed Test")
            success = False
        return success

    def try_solution_train(self, solution, results_info):
        results = [e.try_solution(solution, results_info) for e in self.train_examples]
        return np.all(results)

    def try_solution_test(self, solution, results_info):
        results = [e.try_solution(solution, results_info) for e in self.test_examples]
        return np.all(results)
