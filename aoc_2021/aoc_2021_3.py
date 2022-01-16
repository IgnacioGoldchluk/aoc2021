from collections import Counter
from typing import List, Tuple


def get_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        contents = f.read()
    return contents.split()


def rows_to_columns(rows: List[str]) -> List[str]:
    rows_length = len(rows[0])
    return ["".join(row[pos] for row in rows) for pos in range(0, rows_length)]


def get_bitwise_not(string: str) -> str:
    table = string.maketrans({"1": "0", "0": "1"})
    return string.translate(table)


def get_gamma_epsilon(columns: List[str]) -> Tuple[int]:
    counters = [Counter(column) for column in columns]
    gamma = "".join(max(col, key=lambda bit: counters[i][bit]) for i, col in enumerate(columns))
    epsilon = get_bitwise_not(gamma)
    return int(gamma, base=2), int(epsilon, base=2)


def get_element_as_binary(rows: List[str], criteria: callable, index: int = 0) -> str:
    column = [row[index] for row in rows]
    required_number = criteria(zeros=column.count("0"), ones=column.count("1"))
    valid_combinations = [row for row in rows if row[index] == required_number]
    if len(valid_combinations) == 1:
        return valid_combinations[0]
    else:
        return get_element_as_binary(valid_combinations, criteria, index + 1)


def get_co2_and_oxygen(rows: List[str]) -> Tuple[int]:
    co2 = get_element_as_binary(rows, criteria=lambda zeros, ones: "1" if zeros > ones else "0")
    oxygen = get_element_as_binary(rows, criteria=lambda zeros, ones: "0" if zeros > ones else "1")
    return int(oxygen, 2), int(co2, 2)


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_3.txt")
    gamma, epsilon = get_gamma_epsilon(rows_to_columns(challenge_input))
    print("gamma", gamma, "epsilon", epsilon, "mult", gamma * epsilon)
    oxygen, co2 = get_co2_and_oxygen(challenge_input)
    print("oxygen", oxygen, "co2", co2, "mult", oxygen * co2)
