from typing import List
import numpy as np
import itertools


def get_input(filename: str):
    with open(filename, "r") as f:
        contents = f.read()
    return np.array([[int(x) for x in line] for line in contents.split()])


def octopus_step(matrix):
    matrix += 1


def octopus_flash(matrix):
    # The highest number that a number can go to is the number of elements of the matrix - 1 (itself)
    # Flash_reset makes sure the element that flashed will be negative at the end, that way
    # we can reset it
    flash_reset = (matrix.shape[0] * matrix.shape[1]) * -1
    flashes = 0
    indexes = np.transpose((matrix == 10).nonzero())
    while np.shape(indexes) != (0, 2):
        flashes += np.shape(indexes)[0]
        rows, cols = np.shape(matrix)
        # Add 1 to the 3x3 submatrix (check for edges too)
        for index in indexes:
            row, col = index
            min_row, max_row = max(row - 1, 0), min(row + 2, rows)
            min_col, max_col = max(col - 1, 0), min(col + 2, cols)
            matrix[min_row:max_row, min_col:max_col] += 1
            matrix[row][col] = flash_reset
        # Get all the elements that reached 10 (or more) and keep looping
        indexes = np.transpose((matrix >= 10).nonzero())
    # Reset all the elements
    matrix[matrix < 0] = 0
    return flashes


def count_flashes(matrix, steps: int) -> int:
    flashes = 0
    total_octopus = matrix.shape[0] * matrix.shape[1]
    for step in itertools.count(1):
        octopus_step(matrix)
        flashes_step = octopus_flash(matrix)
        if flashes_step == total_octopus:
            print(f"Every octopus flashed at step {step}!")
            break
        if step <= steps:
            flashes += flashes_step
    return flashes


if __name__ == "__main__":
    matrix = get_input("aoc_2021/2021_11.txt")
    print(count_flashes(matrix, 100))
