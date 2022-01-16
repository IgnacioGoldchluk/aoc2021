from __future__ import annotations
from typing import List, Union
from math import ceil
import itertools

NestedList = Union[List[int], "NestedList"]


class FishNumber:
    def __init__(
        self,
        left: Union[FishNumber, None] = None,
        right: Union[FishNumber, None] = None,
        parent: Union[FishNumber, None] = None,
        value: Union[int, None] = None,
    ):
        self.left = left
        self.right = right
        self.parent = parent
        self.value = value

        if self.left is not None:
            self.left.parent = self
        if self.right is not None:
            self.right.parent = self

    def magnitude(self) -> int:
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def parse_input(filename: str) -> NestedList:
    with open(filename, "r") as f:
        contents = f.read()
    return [eval(line) for line in contents.split("\n")]


def reduce_number(fish_node: FishNumber) -> FishNumber:

    modified = True
    while modified:
        modified = explode_node(fish_node)
        if not modified:
            modified = split_node(fish_node)
    return fish_node


def explode_node(fish_node: FishNumber, depth: int = 0) -> bool:
    if fish_node.value is not None:  # We reached a node without children
        return False

    if depth > 3:
        explode(fish_node)
        return True
    else:
        return explode_node(fish_node.left, depth + 1) or explode_node(fish_node.right, depth + 1)


def split_node(fish_node: FishNumber) -> bool:
    if fish_node.value is None:
        return split_node(fish_node.left) or split_node(fish_node.right)

    if fish_node.value >= 10:
        split(fish_node)
        return True
    return False


def split(fish_node: FishNumber) -> None:
    parent = fish_node.parent
    fish_value = fish_node.value
    left = FishNumber(value=fish_value // 2)
    right = FishNumber(value=int(ceil(fish_value / 2.0)))

    new_node = FishNumber(left=left, right=right, parent=parent)
    left.parent = new_node
    right.parent = new_node

    if fish_node is parent.left:
        parent.left = new_node
    elif fish_node is parent.right:
        parent.right = new_node


def explode(fish_node: FishNumber) -> None:
    explode_to_the_left(fish_node)
    explode_to_the_right(fish_node)

    parent = fish_node.parent
    new_node = FishNumber(value=0, parent=parent)
    if fish_node is parent.left:
        parent.left = new_node
    elif fish_node is parent.right:
        parent.right = new_node


def explode_to_the_left(fish_node: FishNumber):
    # Immediate left is DFS to the right of a parent that has a left
    seen = {fish_node}
    starting_point = fish_node.parent
    while starting_point and starting_point.left in seen:
        seen.add(starting_point)
        starting_point = starting_point.parent

    if not starting_point or not starting_point.left:
        return

    candidate_node = starting_point.left
    while candidate_node.value is None:
        candidate_node = candidate_node.right
    candidate_node.value += fish_node.left.value


def explode_to_the_right(fish_node: FishNumber):
    # Immediate right is DFS to the left of a parent that has a right
    seen = {fish_node}
    starting_point = fish_node.parent
    while starting_point and starting_point.right in seen:
        seen.add(starting_point)
        starting_point = starting_point.parent

    if not starting_point or not starting_point.right:
        return

    candidate_node = starting_point.right
    while candidate_node.value is None:
        candidate_node = candidate_node.left
    candidate_node.value += fish_node.right.value


def add_numbers(current_tree: FishNumber, new_node: FishNumber) -> FishNumber:
    new_fish_node = FishNumber(left=new_node, right=current_tree)
    return reduce_number(new_fish_node)


def add_numbers_list(fish_nodes: List[FishNumber]) -> FishNumber:
    accumulator = add_numbers(fish_nodes[1], fish_nodes[0])
    for number in fish_nodes[2:]:
        accumulator = add_numbers(number, accumulator)
    return accumulator


def list_to_node(numbers_as_list: Union[NestedList, int]) -> FishNumber:
    if isinstance(numbers_as_list, int):
        return FishNumber(value=numbers_as_list)

    left, right = numbers_as_list
    left_val = list_to_node(left)
    right_val = list_to_node(right)
    new_number = FishNumber(left=left_val, right=right_val)
    return new_number


def fish_node_to_list(fish_node: FishNumber) -> NestedList:
    if fish_node.value is not None:
        return fish_node.value

    fish_list = [fish_node_to_list(fish_node.left), fish_node_to_list(fish_node.right)]
    return fish_list


def max_magnitude(numbers: NestedList) -> int:
    maximum = -1
    for pairs in itertools.permutations(numbers, 2):
        if (mag := add_numbers_list([list_to_node(n) for n in pairs]).magnitude()) > maximum:
            maximum = mag
    return maximum


if __name__ == "__main__":
    numbers = parse_input("aoc_2021/2021_18.txt")
    fish_node = add_numbers_list([list_to_node(number) for number in numbers])
    print(fish_node.magnitude())
    print(max_magnitude(numbers))
