from typing import Tuple, List
from functools import reduce


def get_instructions(filename: str) -> List[str]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


def new_position(current_position: Tuple[int], instruction: str) -> Tuple[int]:
    instruction = instruction.split(" ")
    number = int(instruction[1])
    depth, position = current_position
    if instruction[0] == "forward":
        return (depth, position + number)
    if instruction[0] == "up":
        return (depth - number, position)
    if instruction[0] == "down":
        return (depth + number, position)


def new_position_with_aim(current_position: Tuple[int], instruction: str) -> Tuple[int]:
    instruction = instruction.split(" ")
    number = int(instruction[1])
    depth, position, aim = current_position
    if instruction[0] == "forward":
        return (depth + number * aim, position + number, aim)
    if instruction[0] == "up":
        return (depth, position, aim - number)
    if instruction[0] == "down":
        return (depth, position, aim + number)


def final_position(instructions: List[str]) -> Tuple[int]:
    return reduce(new_position, instructions, (0, 0))


def final_position_with_aim(instructions: List[str]) -> Tuple[int]:
    return reduce(new_position_with_aim, instructions, (0, 0, 0))


if __name__ == "__main__":
    instructions = get_instructions("aoc_2021/2021_2.txt")
    depth, position = final_position(instructions)
    print(depth * position)

    depth, position, _ = final_position_with_aim(instructions)
    print(depth * position)
