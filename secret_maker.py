import json

import numpy as np

from utils import tasks, load_task
from task import Task, Example

def make_secret_pour():
    task_file = tasks["pour"]
    task_dict = load_task(f"data/training/{task_file}")
    task = Task(task_dict)

    grid = np.array(task.train_examples[1].input_grid.grid)
    new_grid = np.concatenate((grid[:,2:],grid[:,:2]), axis=1)

    out_grid = Example({"input":new_grid,"output":new_grid},0,"Secret").generate_solution("solution_2")

    task_dict["test"].append(
        {"input":new_grid.astype(np.int64).tolist(),"output":out_grid.astype(np.int64).tolist()}
    )
    file_path = "secret_tests/pour.json"
    with open(file_path, 'w') as json_file:
        json.dump(task_dict, json_file, indent=None)


def make_secret_lines():
    task_file = tasks["lines"]
    task_dict = load_task(f"data/training/{task_file}")

    new_grid = np.zeros((3,50)).astype(np.int64)
    new_grid[0,15] = 5
    new_grid[0,24] = 9


    out_grid = Example({"input": new_grid, "output": new_grid}, 0, "Secret").generate_solution("solution_1")

    task_dict["test"].append(
        {"input": new_grid.astype(np.int64).tolist(), "output": out_grid.astype(np.int64).tolist()}
    )
    file_path = "secret_tests/lines.json"
    with open(file_path, 'w') as json_file:
        json.dump(task_dict, json_file, indent=None)

if __name__ == "__main__":
    make_secret_lines()

