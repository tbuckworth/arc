import json

import numpy as np

from main import tasks, load_task
from task import Task, Example

if __name__ == "__main__":
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

    print(out_grid)