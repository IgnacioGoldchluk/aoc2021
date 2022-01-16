from typing import List, Tuple, Dict
from functools import reduce
from collections import defaultdict

coords_dict = Dict[Tuple[int, int], int]


def parse(input: str) -> Tuple[coords_dict, List[str]]:
    coords = defaultdict(int)
    points, folds = input.split("\n\n")
    for point in points.split("\n"):
        key = tuple(int(x) for x in point.split(","))
        coords[key] = 1
    return coords, folds.split("\n")


def fold(coords: coords_dict, fold_instruction: str) -> coords_dict:
    fold_line, index = fold_instruction.replace("fold along ", "").split("=")
    if fold_line == "x":
        return fold_left(coords, int(index))
    elif fold_line == "y":
        return fold_up(coords, int(index))


def fold_left(coords: coords_dict, index: int) -> coords_dict:
    for point in list(coords.keys()):
        x, y = point
        if x > index:
            coords[(2 * index - x, y)] += 1
            del coords[(x, y)]
    return coords


def fold_up(coords: coords_dict, index: int) -> coords_dict:
    for point in list(coords.keys()):
        x, y = point
        if y > index:
            coords[(x, 2 * index - y)] += 1
            del coords[(x, y)]
    return coords


def multiple_folds(coords: coords_dict, folds: List[str]) -> coords_dict:
    return reduce(lambda accum, fold_instruction: fold(accum, fold_instruction), folds, coords)


def print_code(coords: coords_dict) -> None:
    max_x = max(p[0] for p in coords)
    max_y = max(p[1] for p in coords)
    for y in range(0, max_y + 1):
        print("".join(["#" if coords.get((x, y), 0) > 0 else " " for x in range(0, max_x + 1)]))


if __name__ == "__main__":
    with open("aoc_2021/2021_13.txt", "r") as f:
        input = f.read()

    coords, folds = parse(input)
    folded = multiple_folds(coords, folds)
    print_code(folded)
