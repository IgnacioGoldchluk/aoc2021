from typing import List


def get_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        contents = f.read()
    return list(map(int, contents.split(",")))


def get_median(numbers: List[int]) -> int:
    length = len(numbers)
    sorted_list = sorted(numbers)
    index = (length - 1) // 2
    return sorted_list[index]


def get_mean(numbers: List[int]) -> int:
    return int(round(sum(numbers) / len(numbers)))


def sum_up_to_n(n: int) -> int:
    return (n + 1) * (n) // 2


def get_fuel_exponential(numbers: List[int], point: int) -> int:
    return sum(map(lambda current_pos: sum_up_to_n(abs(point - current_pos)), numbers))


def get_fuel(list_of_numbers, point):
    return sum(map(lambda current_pos: abs(point - current_pos), list_of_numbers))


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_7.txt")
    print(get_fuel(challenge_input, get_median(challenge_input)))
    mean = get_mean(challenge_input)
    minimum = min(
        get_fuel_exponential(challenge_input, point) for point in range(mean - 1, mean + 2)
    )
    print(minimum)
