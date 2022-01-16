from typing import List, Dict
from collections import Counter
from functools import reduce


def get_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        contents = f.read()
    return list(map(int, contents.split(",")))


def build_initial_fish_dict(input: List[int]) -> Dict[int, int]:
    return Counter(input)


def next_day(starting_dict: Dict[int, int]) -> Dict[int, int]:
    # All elements move one number below
    new_dict = {day - 1: count for day, count in starting_dict.items()}
    # Move the fishes that were in 0 (now -1) to the value 6, and also add the new fish with 8 days left
    new_fish = new_dict.pop(-1, 0)
    new_dict.setdefault(6, 0)
    new_dict[6] += new_fish
    new_dict[8] = new_fish
    return new_dict


def final_population(input: List[int], number_of_days: int) -> int:
    final_dict = reduce(
        lambda curr_dict, _: next_day(curr_dict),
        range(number_of_days),
        build_initial_fish_dict(input),
    )
    return sum(final_dict.values())


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_6.txt")
    print(final_population(challenge_input, 80))
    print(final_population(challenge_input, 256))
