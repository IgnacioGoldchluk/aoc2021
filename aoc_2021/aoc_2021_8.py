from typing import List, Set, Tuple, Dict
from collections import defaultdict
from collections import Counter
from functools import reduce

SEVEN_SEGMENT_TABLE = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def get_a(count_dict: Dict[int, str]) -> Dict[str, str]:
    return {"a": list(set(count_dict[3][0]) - set(count_dict[2][0]))[0]}


def get_g_d(count_dict: Dict[int, str], counter: Dict[str, int]) -> Dict[str, str]:
    dict_to_return = dict()
    # Now get g and d, they are both length 7 but g is in every length 6 number, d in only 2
    g_and_d = {c for c, count in counter.items() if count == 7}

    sets = [set(x) for x in count_dict[6]]
    set_and = reduce(lambda accum, curr: accum & curr, sets)
    dict_to_return["g"] = list(g_and_d & set_and)[0]
    dict_to_return["d"] = list(g_and_d - set([dict_to_return["g"]]))[0]
    return dict_to_return


def get_rest_of_elements(counter: Dict[str, int]):
    map_dict = {"e": 4, "f": 9, "b": 6, "c": 8}
    reverse_counter = {val: key for key, val in counter.items()}
    return {key: reverse_counter[val] for key, val in map_dict.items()}


def make_conversion_dict(read_numbers: List[str]) -> Dict[str, str]:
    conversion_dict = dict()
    count_dict = defaultdict(list)
    for element in read_numbers:
        count_dict[len(element)].append(element)
    # First get a, which is the difference between 7 (length==3) and 1 (length==2)
    conversion_dict.update(get_a(count_dict))
    read_numbers_str = "".join(read_numbers)
    counter = Counter(read_numbers_str)
    conversion_dict.update(get_g_d(count_dict, counter))

    # Remove all the elements
    for key in conversion_dict.values():
        counter.pop(key)
    # We now have all unique elements with length
    conversion_dict.update(get_rest_of_elements(counter))
    return {val: key for key, val in conversion_dict.items()}


def get_input(filename: str) -> List[Tuple[str]]:
    with open(filename, "r") as f:
        contents = f.read()
    return format_input(contents)


def format_input(contents: str) -> List[List[str]]:
    return [get_lists_from_delimiter(x.split(), "|") for x in contents.split("\n")]


def get_lists_from_delimiter(list_with_delimiter: List[str], delimiter: str) -> Tuple[List[str]]:
    index_of_delimiter = list_with_delimiter.index(delimiter)
    return (list_with_delimiter[:index_of_delimiter], list_with_delimiter[index_of_delimiter + 1 :])


def count_elements_with_length_in_display(display_input: List[str], lengths: Set[int]) -> int:
    return sum(len(digit) in lengths for digit in display_input)


def count_total_elements_with_length(challenge_input: List[List[str]], lengths: Set[int]) -> int:
    displays = [inputs[1] for inputs in challenge_input]
    return sum(count_elements_with_length_in_display(display, lengths) for display in displays)


def decode(samples: List[str], display_val: List[str]) -> int:
    conversion_dict = make_conversion_dict(samples)
    return int("".join(display_to_digit(digit, conversion_dict) for digit in display_val))


def display_to_digit(display: str, conversion_dict: Dict[str, str]) -> str:
    translator = display.maketrans(conversion_dict)
    return SEVEN_SEGMENT_TABLE["".join(sorted(display.translate(translator)))]


def sum_of_decode(challenge_input: List[List[str]]) -> int:
    return sum(decode(x[0], x[1]) for x in challenge_input)


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_8.txt")
    print(count_total_elements_with_length(challenge_input, {2, 3, 4, 7}))
    print(sum_of_decode(challenge_input))
