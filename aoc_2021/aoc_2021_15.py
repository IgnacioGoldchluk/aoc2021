from typing import List, Dict, Tuple
import heapq
from collections import defaultdict
import itertools

Matrix = Dict[Tuple[int, int], int]


def get_input(filename: str) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    return contents


def parse(input_matrix: str) -> Matrix:
    coords_dict = dict()
    for x, row in enumerate(input_matrix.split("\n")):
        for y, val in enumerate(row):
            coords_dict[(x, y)] = int(val)
    return coords_dict


def adjacent_points(matrix, point):
    possibilities = [
        (point[0] - 1, point[1]),
        (point[0], point[1] - 1),
        (point[0] + 1, point[1]),
        (point[0], point[1] + 1),
    ]
    return [p for p in possibilities if p in matrix]


def find_shortest_path(matrix: Matrix, start: int, end: int) -> int:
    visited = set()
    priority_queue = []
    costs = defaultdict(lambda: float("inf"))
    costs[start] = 0
    heapq.heappush(priority_queue, (0, start))

    while priority_queue:
        _, point = heapq.heappop(priority_queue)
        visited.add(point)

        for adjacent_point in adjacent_points(matrix, point):
            if adjacent_point in visited:
                continue
            weight = matrix[adjacent_point]
            new_cost = costs[point] + weight
            if new_cost < costs[adjacent_point]:
                costs[adjacent_point] = new_cost
                heapq.heappush(priority_queue, (new_cost, adjacent_point))
    return costs[end]


def expand_matrix(matrix: Matrix, n_of_times: int) -> Matrix:
    starting_points = list(matrix.keys())
    width, height = max(starting_points)
    width += 1
    height += 1

    for point in starting_points:
        x, y = point
        starting_value = matrix[point]
        for inc_x, inc_y in itertools.product(range(n_of_times), range(n_of_times)):
            addition = inc_x + inc_y
            if not addition:
                continue
            matrix[(x + inc_x * width, y + inc_y * height)] = ((starting_value + addition) % 10) + (
                (starting_value + addition) // 10
            )
    return matrix


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_15.txt")
    matrix = parse(challenge_input)
    end_point = max(matrix)
    print(end_point)
    print(find_shortest_path(matrix, (0, 0), end_point))
    matrix = expand_matrix(matrix, n_of_times=5)
    end_point = max(matrix)
    print(end_point)
    print(find_shortest_path(matrix, (0, 0), end_point))
