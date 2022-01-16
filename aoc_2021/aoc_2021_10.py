from typing import List, Union, Tuple
from functools import reduce

PAIRS_DICT = {")": "(", "]": "[", "}": "{", ">": "<"}
OPPOSITE_PAIRS_DICT = {val: key for key, val in PAIRS_DICT.items()}
OPENING_CHARS = list(PAIRS_DICT.values())
POINTS_PER_CORRUPTED_CHAR = {")": 3, "]": 57, "}": 1197, ">": 25137}
POINTS_PER_COMPLETION_CHAR = {")": 1, "]": 2, "}": 3, ">": 4}


class Stack(list):
    def push(self, element):
        self.append(element)


def get_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        contents = f.read()
    return contents.split()


def get_completion_corrupted_characters(lines: List[str]) -> Tuple[List[str], List[List[str]]]:
    corrupted_and_completion = list(map(get_chars, lines))
    corrupted = [x for x in corrupted_and_completion if isinstance(x, str)]
    completion = [x for x in corrupted_and_completion if isinstance(x, list)]
    return completion, corrupted


def get_chars(line: str) -> Union[List[str], str]:
    stack = Stack()

    for character in line:
        if character in OPENING_CHARS:
            stack.push(character)
        else:
            expected_character = PAIRS_DICT[character]
            if expected_character != stack.pop():
                return character
    return [OPPOSITE_PAIRS_DICT[char] for char in reversed(stack)]


def get_score_from_corrupted_characters(corrupted_characters: List[str]) -> int:
    return sum(POINTS_PER_CORRUPTED_CHAR[char] for char in corrupted_characters)


def get_score_from_completion_characters(completion: List[List[str]]) -> int:
    scores = list(
        map(
            lambda completion_seq: reduce(
                lambda accum, current: accum * 5 + POINTS_PER_COMPLETION_CHAR[current],
                completion_seq,
                0,
            ),
            completion,
        )
    )
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    lines = get_input("aoc_2021/2021_10.txt")
    completion, corrupted = get_completion_corrupted_characters(lines)
    print(get_score_from_corrupted_characters(corrupted))
    print(get_score_from_completion_characters(completion))
