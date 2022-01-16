from typing import List, Tuple, Iterable
import itertools
from collections import Counter


def get_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        contents = f.readlines()
    return contents


def coords_to_tuples(coords: str) -> Tuple[Tuple[int]]:
    start, finish = coords.split(" -> ")
    start = tuple(int(x) for x in start.split(","))
    finish = tuple(int(x) for x in finish.split(","))

    return start, finish


def tuples_to_points(tuples: Tuple[Tuple[int]], include_diagonals: bool) -> List[Tuple[int]]:
    start, finish = tuples
    if start[0] == finish[0]:
        return vertical_line_points(start, finish)
    elif start[1] == finish[1]:
        return horizontal_line_points(start, finish)
    else:
        return diagonal_line_points(start, finish) if include_diagonals else []


def vertical_line_points(start: Tuple[int], finish: Tuple[int]) -> List[Tuple[int]]:
    range_y = build_range(start[1], finish[1])
    point_x = start[0]
    return [(point_x, point_y) for point_y in range_y]


def horizontal_line_points(start: Tuple[int], finish: Tuple[int]) -> List[Tuple[int]]:
    range_x = build_range(start[0], finish[0])
    point_y = start[1]
    return [(point_x, point_y) for point_x in range_x]


def diagonal_line_points(start: Tuple[int], finish: Tuple[int]) -> List[Tuple[int]]:
    range_x = build_range(start[0], finish[0])
    range_y = build_range(start[1], finish[1])
    return [(point_x, point_y) for point_x, point_y in zip(range_x, range_y)]


def build_range(start_ax: int, finish_ax: int) -> Iterable:
    ascending = start_ax < finish_ax
    offset_finish = 1 if ascending else -1
    step = offset_finish
    return range(start_ax, finish_ax + offset_finish, step)


def solve(input: List[str], include_diagonals: bool) -> int:
    total_points = list(
        itertools.chain.from_iterable(
            tuples_to_points(coords_to_tuples(coords), include_diagonals) for coords in input
        )
    )
    counter = Counter(total_points)

    return sum(map(lambda occurrences: occurrences > 1, counter.values()))


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_5.txt")
    for include_diagonals in (False, True):
        print(solve(challenge_input, include_diagonals=include_diagonals))
