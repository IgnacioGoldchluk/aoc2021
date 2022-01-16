from typing import List


def get_input(filename) -> List[int]:
    with open(filename, "r") as f:
        contents = f.read()
    return list(map(int, contents.split()))


def count_decreases(measurements: List[int]) -> int:
    return sum(map(lambda x, y: x < y, measurements[:-1], measurements[1:]))


def accumulate_measurements(measurements: List[int], groups: int) -> List[int]:
    return list(map(sum, [measurements[n : n + groups] for n in range(0, len(measurements))]))


if __name__ == "__main__":
    measurements = get_input("aoc_2021/2021_1.txt")
    print(count_decreases(measurements))
    print(count_decreases((accumulate_measurements(measurements, groups=3))))
