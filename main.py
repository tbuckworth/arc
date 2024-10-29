import json
from pickle import FALSE

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def load_jsons():

    # Load a single ARC task
    with open('data/training/0a938d79.json') as f:
        task = json.load(f)

    # Example of accessing input/output grids for the first example
    input_grid = task['train'][0]['input']
    output_grid = task['train'][0]['output']

    rgb_grid = array_and_plot_grid(input_grid)
    array_and_plot_grid(output_grid)

    grid = np.array(input_grid)
    col_grid = colour_lookup()[grid]

    str_grid = np.array([[f"cell_colour({i},{j},{col_grid[i, j]})." for j in range(grid.shape[1])] for i in range(grid.shape[0])])


    return


def array_and_plot_grid(input_grid):
    rgb_grid = grid2rgb(input_grid)
    plot_grid(rgb_grid)
    return rgb_grid


def grid2rgb(input_grid):
    grid = np.array(input_grid)
    rgb_grid = rgb_lookup()[grid]
    return rgb_grid


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_jsons()

