from typing import Callable, Dict, Set, Tuple
import re
from scipy.spatial import distance

Point = Tuple[int, int, int]


def get_input(filename: str) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    return contents


def parse_input(challenge_input: str) -> Dict[int, Set[Point]]:
    scanner_points = dict()
    scanner_inputs = challenge_input.split("\n\n")
    scanner_pattern = re.compile(r"--- scanner (\d+) ---")

    for scanner_input in scanner_inputs:
        scanner_line, *coords = scanner_input.split("\n")
        scanner_number = int(scanner_pattern.search(scanner_line).group(1))
        scanner_points[scanner_number] = {tuple(map(int, coord.split(","))) for coord in coords}
    return scanner_points


if __name__ == "__main__":
    file_contents = get_input("aoc_2021/2021_19.txt")
    scanner_dict = parse_input(file_contents)
