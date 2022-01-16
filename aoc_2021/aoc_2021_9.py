from typing import List, Tuple, Set
from collections import deque
from functools import reduce


def get_input(filename: str) -> List[List[int]]:
    with open(filename, "r") as f:
        contents = f.read()
    return [[int(num) for num in nums] for nums in contents.split()]


def get_local_minimums_and_basins(matrix: List[List[int]]) -> Tuple[List[int], Set[Tuple[int]]]:
    local_minimums = []
    basins = []
    for row_idx, row in enumerate(matrix):
        for col_idx, val in enumerate(row):
            if is_minimum(row_idx, col_idx, matrix):
                local_minimums.append(val)
                basins.append(basin_from_minimum(row_idx, col_idx, matrix))
    return local_minimums, basins


def basin_from_minimum(row_idx: int, col_idx: int, matrix: List[List[int]]) -> Set[Tuple[int]]:
    basin = {(row_idx, col_idx)}
    points_queue = deque(get_non_9_adjacent_points(row_idx, col_idx, matrix))
    while points_queue:
        row, col = points_queue.pop()
        basin.add((row, col))
        points_queue.extend(
            p for p in get_non_9_adjacent_points(row, col, matrix) if not p in basin
        )
    return basin


def get_non_9_adjacent_points(
    row_idx: int, col_idx: int, matrix: List[List[int]]
) -> List[Tuple[int]]:
    return [p for p in get_adjacent_points(row_idx, col_idx, matrix) if matrix[p[0]][p[1]] != 9]


def is_minimum(row_idx: int, col_idx: int, matrix: List[List[int]]) -> int:
    number = matrix[row_idx][col_idx]
    points_indexes = get_adjacent_points(row_idx, col_idx, matrix)
    return all(number < matrix[point[0]][point[1]] for point in points_indexes)


def get_adjacent_points(row_idx: int, col_idx: int, matrix: List[List[int]]) -> Set[Tuple[int]]:
    min_row, max_row = max(row_idx - 1, 0), min(row_idx + 1, len(matrix) - 1)
    min_col, max_col = max(col_idx - 1, 0), min(col_idx + 1, len(matrix[0]) - 1)
    return {(min_row, col_idx), (max_row, col_idx), (row_idx, max_col), (row_idx, min_col)} - {
        (row_idx, col_idx)
    }


def basins_score(basins: Set[Tuple[int]]) -> int:
    return reduce(lambda accum, val: accum * val, sorted(len(basin) for basin in basins)[-3:])


def minimums_score(minimums: List[int]) -> int:
    return sum(x + 1 for x in minimums)


if __name__ == "__main__":
    matrix = get_input("aoc_2021/2021_9.txt")
    minimums, basins = get_local_minimums_and_basins(matrix)
    print(minimums_score(minimums))
    print(basins_score(basins))
