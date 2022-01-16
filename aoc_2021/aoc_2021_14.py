from typing import Tuple, Dict
from collections import Counter

memoization = dict()
poly_dict = Dict[str, str]


def get_input(filename: str) -> Tuple[str, Dict[str, str]]:
    with open(filename, "r") as f:
        contents = f.read()
    string, to_dict = contents.split("\n\n")
    mapping_dict = dict()
    for string_map in to_dict.split("\n"):
        chain, insert = string_map.split(" -> ")
        mapping_dict[chain] = insert
    return string, mapping_dict


def get_total_count(initial_value: str, insertion_dict: poly_dict, steps: int) -> Counter:
    counter = Counter()
    chunks = [initial_value[x : x + 2] for x in range(len(initial_value) - 1)]
    for chunk in chunks:
        counter.update(get_expanded_count(chunk, insertion_dict, steps))
    # All the middle elements will be repeated once in the initial chunks,
    # they are removed later in the recursive function, so we only have to
    # subtract them here
    middle_elements = initial_value[1:-1]
    counter.subtract(Counter(middle_elements))
    return counter


def get_expanded_count(initial_value: str, insertion_dict: poly_dict, steps_left: int) -> Counter:
    if not steps_left:
        return Counter(initial_value)

    if value := memoization.get((initial_value, steps_left)):
        return value

    mapping = insertion_dict[initial_value]
    # Insert the mapped element in the initial pair
    expanded_value = initial_value[0] + mapping + initial_value[1]
    chunks = [expanded_value[x : x + 2] for x in range(len(expanded_value) - 1)]

    counter = Counter()
    for chunk in chunks:
        counter.update(get_expanded_count(chunk, insertion_dict, steps_left - 1))
    counter.subtract(Counter(expanded_value[1]))
    memoization[(initial_value, steps_left)] = counter
    return counter


if __name__ == "__main__":
    string, insertion_dict = get_input("aoc_2021/2021_14.txt")
    counter = get_total_count(string, insertion_dict, 40)
    print(max(counter.values()) - min(counter.values()))
