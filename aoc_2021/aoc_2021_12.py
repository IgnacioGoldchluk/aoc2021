from typing import List, Dict, Set
from collections import Counter, defaultdict


def get_input(filename: str) -> List[str]:
    with open(filename, "r") as f:
        contents = f.read()
    return contents.split()


def parse(challenge_input: List[str]) -> Dict[str, Set[str]]:
    nodes_dict = defaultdict(set)
    for line in challenge_input:
        node1, node2 = line.split("-")
        nodes_dict[node1].add(node2)
        nodes_dict[node2].add(node1)
    return nodes_dict


def total_paths(caves: Dict[str, Set[str]], start: str, end: str, path_func) -> List[List[str]]:
    paths = []
    traverse(caves, start, end, [start], paths, path_func)
    return len(paths)


def traverse(
    caves_dict: Dict[str, Set[str]],
    current_cave: str,
    end: str,
    path: List[str],
    paths: List[List[str]],
    invalid_path_func,
):
    for cave in caves_dict[current_cave]:
        if cave == end:
            paths.append(path + [end])
        elif invalid_path_func(cave, tuple(path)) or cave == path[0]:
            continue
        else:
            traverse(caves_dict, cave, end, path + [cave], paths, invalid_path_func)


def is_lowercase_cave(cave_name: str) -> bool:
    return cave_name.islower() and not cave_name in ("start", "end")


def is_path_invalid(cave, current_path):
    return is_lowercase_cave(cave) and current_path.count(cave) == 1


def is_path_invalid2(cave, current_path):
    lowercase_caves = list(filter(is_lowercase_cave, current_path))
    counter = Counter(lowercase_caves)
    return counter.get(cave, 0) == 2 or (
        any(counter.get(c, 0) == 2 for c in lowercase_caves) and cave in lowercase_caves
    )


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_12.txt")
    caves = parse(challenge_input)
    print(total_paths(caves, "start", "end", path_func=is_path_invalid))
    print(total_paths(caves, "start", "end", path_func=is_path_invalid2))
