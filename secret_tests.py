import json
import os
import time
import unittest

from helper_check import check, all_singletons
from utils import load_task, tasks
from task import Task


class TaskTester(unittest.TestCase):

    def try_solution(self, task_file, solution):
        results_dir = 'test_results_info.json'
        if os.path.exists(results_dir):
            with open(results_dir, 'r') as file:
                test_results_info = json.load(file)
        else:
            test_results_info = []
        print(f"\n{solution}")
        task_dict = load_task(f"secret_tests/{task_file}.json")
        task = Task(task_dict, solution)
        start = time.time()
        res = task.try_solution(solution, test_results_info)
        elapsed = time.time() - start
        test_results_info.append([
            {"score": f"{elapsed:.4f}s","name":f"{solution} time", "possible":"NA"}
        ])
        # self.assertTrue(res)
        with open(results_dir, 'w') as json_file:
            json.dump(test_results_info, json_file, indent=4)

    def add_to_results(self, outputs):
        results_dir = 'test_results_info.json'
        if os.path.exists(results_dir):
            with open(results_dir, 'r') as file:
                test_results_info = json.load(file)
        else:
            test_results_info = []
        test_results_info += outputs
        with open(results_dir, 'w') as json_file:
            json.dump(test_results_info, json_file, indent=4)

    def test_singletons(self):
        singles = all_singletons()
        print('\n'.join(singles))
        result = {"score":3-len(singles),"name":"No Singletons","possible":3}
        self.add_to_results([result])

    def test_helpers(self):
        self.add_to_results(check())

    def test_solution_1(self):
        self.try_solution("lines", 'solution_1')

    def test_solution_2(self):
        self.try_solution("pour", 'solution_2')

if __name__ == '__main__':
    unittest.main()
