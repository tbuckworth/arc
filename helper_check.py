import os
import re

from utils import run_prolog_program

def helpers_template(fill):
    return f"""
input_colour(0,0,black).
input_colour(0,1,black).
input_colour(1,0,black).
input_colour(1,1,black).

print_results:-{fill}
[helpers], print_results, halt.
"""

def run_code(test):
    prolog_dir = "prolog"
    if not os.path.exists(prolog_dir):
        prolog_dir = "../provided/prolog"
    test_program = helpers_template(test)
    test_filename = f"tst_input_file"
    test_file = os.path.join(prolog_dir, f"{test_filename}.pl")
    with open(test_file, 'w') as file:
        file.write(test_program)
    program = f"[{test_filename}], [helpers], print_results, halt."
    out_prolog = run_prolog_program(program=program, curr_dir=prolog_dir)
    os.remove(test_file)
    return out_prolog


def check():
    tests = {
    "all_rows":"""
    all_rows(Rs),
    length(Rs, N),
    write('all_rows:'), write(N), write('/2'), nl.
    ""","all_cols":"""
    all_cols(Cs),
    length(Cs, M),
    write('all_cols:'), write(M), write('/2'), nl.
    ""","nrow":"""
    nrow(N2),
    write('nrow:'), write(N2), write('/2'), nl.
    ""","ncol":"""
    ncol(M2),
    write('ncol:'), write(M2), write('/2'), nl.
    ""","min":"""
    min([11,-22,33,0,54,107],Min),
    write('min:'), write(Min), write('/-22'), nl.
    ""","max":"""
    max([11,-22,33,0,54,107],Max),
    write('max:'), write(Max), write('/107'), nl.
    """
    }
    results = []
    for name, test in tests.items():
        res = run_code(test)
        score = 0
        if res is not None:
            search = re.search(r":(.*)/(.*)", res)
            n = search.group(1)
            m = search.group(2)
            if n == m:
                score = 1
                print(f"{name}: answer:{n}, correct:{m} - Succeeded")
            else:
                print(f"{name}: answer:{n}, correct:{m} - Failed")
        else:
            print(f"{name}: Error - Failed")

        results.append(
            {"score":score,
             "name":f"helpers:{name}",
             "possible":1}
        )
    return results

def singletons(file):
    program = f"[{file}], halt."
    out_prolog = run_prolog_program(program=program, curr_dir="prolog", return_err=True)
    lines = out_prolog.split('\n')
    s_lines = [i for i, l in enumerate(lines) if re.search("singleton",l)]
    singles = []
    for i in s_lines:
        x = lines[i] + " " + re.sub("'.*/.*prolog","'prolog",lines[i+1])
        singles.append(x)
    return singles

def all_singletons():
    singles = singletons("helpers")
    singles += singletons("solution_1")
    singles += singletons("solution_2")
    return singles


if __name__ == "__main__":
    all_singletons()
