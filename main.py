import copy
import json
from pickle import FALSE

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

tasks = {
    "lines": "0b148d64.json",
    "grids": "90f3ed37.json",
    "pour": "d4f3cd78.json",
    "cross": "e21d9049.json",
    "stripes": "f8c80d96.json"
}


def run_prolog_program(program, curr_dir=""):
    # Construct the command to run SICStus Prolog
    command = ['/usr/local/sicstus4.8.0/bin/sicstus', '--noinfo', '--goal', program]

    # Execute the command
    # result = subprocess.run(command, capture_output=True, text=True, cwd=curr_dir)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=curr_dir,
            timeout=30  # Timeout after 30 seconds
        )
        if result.returncode != 0:
            print("SICStus Prolog reported an error:")
            return result.stderr
        else:
            # Print the output
            return result.stdout
    except subprocess.TimeoutExpired:
        print("SICStus Prolog timed out.")
        return None

def hex_to_rgb(hex_color):
    # Remove the '#' character if it exists
    hex_color = hex_color.lstrip('#')
    # Convert the hexadecimal values to RGB tuple
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# # Example usage
# hex_color = "#34A2FE"
# rgb_color = hex_to_rgb(hex_color)
# print("RGB Color:", rgb_color)

def plot_grid(rgb_grid):
    height, width = rgb_grid.shape[:2]

    # Create a plot with gridlines
    fig, ax = plt.subplots()

    # Display the RGB grid
    ax.imshow(rgb_grid, extent=(0, width, 0, height), interpolation='none')

    # Set gridlines and customize appearance
    ax.set_xticks(np.arange(0.001, width, 1), minor=True)
    ax.set_yticks(np.arange(0.001, height, 1), minor=True)
    ax.grid(which='minor', color='grey', linestyle='-', linewidth=1)

    # Hide major ticks and labels
    ax.tick_params(which='major', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.tick_params(which='minor', bottom=False, left=False)

    # Remove extra whitespace
    plt.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    ax.set_aspect('equal')  # Ensure pixels are square

    plt.show()


def rgb_lookup():
    df = pd.read_csv("colours.csv")
    return np.array(df['colour'].apply(lambda x: tuple(int(x[i:i + 2], 16) for i in (0, 2, 4))).values.tolist())


def colour_lookup():
    df = pd.read_csv("colours.csv")
    return df['name'].values


def nd_sort(arr):
    # Reshape the array to a 2D array where each row represents a combination of indices and values
    D1, D2, D3 = arr.shape
    arr_flat = arr.reshape(-1, D3)

    # Create index arrays for the first two dimensions
    idx0, idx1 = np.meshgrid(np.arange(D1), np.arange(D2), indexing='ij')
    idx0 = idx0.flatten()
    idx1 = idx1.flatten()

    # Combine indices and values
    combined = np.column_stack((idx0, idx1, arr_flat))

    # Sort based on the first two indices
    sorted_indices = np.lexsort((combined[:, 1], combined[:, 0]))
    sorted_combined = combined[sorted_indices]

    # Reshape back to the original array shape if needed
    sorted_arr = sorted_combined[:, 2:].reshape(D1, D2, D3)
    return sorted_arr


def FOL2prolog(preds):
    return '\n'.join(['\n'.join(x) for x in preds])


def prolog2FOL_array(prolog):
    arr = np.array(prolog.split('\n'))
    return arr[arr != '']


def FOL2grid(preds):
    preds = preds.reshape(-1)
    # will fail if missing preds (all squares need to specify a colour)
    preds = np.char.replace(preds, r"output_colour(", "")
    preds = np.char.replace(preds, r").", "")
    strs = np.array(np.char.split(preds, ",").tolist())
    idx = strs[..., :2].astype(int)
    col_val = colour_names2idx(strs[..., -1])

    # shape = idx.max(0) + 1
    # idx_1d = idx[..., 0] * shape[1] + idx[..., 1]
    # col_val[idx_1d].reshape(shape)

    out = np.zeros(idx.max(0) + 1)
    for i in range(len(idx)):
        out[tuple(idx[i])] = col_val[i]

    return out


def colour_names2idx(colour_names):
    df = pd.read_csv("colours.csv")
    colour_to_idx = {colour: idx for idx, colour in zip(df.int, df.name)}
    # Vectorize the mapping function
    vectorized_mapping = np.vectorize(colour_to_idx.get)
    # Apply the mapping to the 2D array
    arr_idx = vectorized_mapping(colour_names)
    return arr_idx


def load_jsons():
    # Load a single ARC task
    task = load_task()


def load_task(json_file='data/training/0a938d79.json'):
    with open(json_file) as f:
        task = json.load(f)
    return task


def grid2FOL(input_grid, prefix):
    grid = np.array(input_grid)
    col_grid = colour_lookup()[grid]
    str_grid = np.array(
        [[f"{prefix}_colour({i},{j},{col_grid[i, j]})." for j in range(grid.shape[1])] for i in range(grid.shape[0])])
    return str_grid


def array_and_plot_grid(input_grid):
    rgb_grid = grid2rgb(input_grid)
    plot_grid(rgb_grid)
    return rgb_grid


def grid2rgb(input_grid):
    grid = np.array(input_grid).astype(np.int64)
    rgb_grid = rgb_lookup()[grid]
    return rgb_grid


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_jsons()
