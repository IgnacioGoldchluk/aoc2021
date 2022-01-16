from typing import Tuple, Dict, List, Literal
import itertools

ImgValues = Literal["#", "."]
Point = Tuple[int, int]
Image = Dict[Point, ImgValues]
PositionMap = List[ImgValues]


def get_input(filename: str) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    return contents


def parse(challenge_input: str) -> Tuple[PositionMap, Image]:
    position_map, image = challenge_input.split("\n\n")

    image_dict = dict()
    for row_idx, row in enumerate(image.split("\n")):
        for col_idx, val in enumerate(row):
            image_dict[(row_idx, col_idx)] = val

    return position_map, image_dict


def enhance_point(
    image: Image, existing_point: Point, position_map: PositionMap, filler: ImgValues
) -> ImgValues:
    x, y = existing_point
    string = "".join(
        image.get((xp, yp), filler)
        for xp, yp in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2))
    )
    position = int(string.replace("#", "1").replace(".", "0"), 2)
    return position_map[position]


def fill_borders(new_dict: Image, filler: ImgValues) -> None:
    points = list(new_dict.keys())
    min_x, min_y = min(points)
    max_x, max_y = max(points)

    # Left and right borders
    for x in range(min_x - 1, max_x + 2):
        new_dict[(x, min_y - 1)] = filler
        new_dict[(x, max_y + 1)] = filler
    # Bottom and top borders
    for y in range(min_y - 1, max_y + 2):
        new_dict[(max_x + 1, y)] = filler
        new_dict[(min_x - 1, y)] = filler


def enhance(image: Image, position_map: PositionMap, filler: ImgValues) -> Image:
    fill_borders(image, filler)
    enhanced_dict = {
        point: enhance_point(image, point, position_map, filler) for point in image.keys()
    }
    next_filler = get_next_filler(position_map, filler)

    return enhanced_dict, next_filler


def get_next_filler(position_map: PositionMap, current_filler: ImgValues) -> ImgValues:
    all_filled = "".join([current_filler] * 9).replace("#", "1").replace(".", "0")
    if position_map[int(all_filled, 2)] == "#":
        # Change the filler, otherwise it will keep expanding
        return "." if current_filler == "#" else "#"
    else:
        return "."


def enhance_and_count_lit_pixels(image: Image, position_map: PositionMap, steps: int) -> int:
    new_image, next_filler = enhance(image, position_map, ".")
    for _ in range(1, steps):
        new_image, next_filler = enhance(new_image, position_map, next_filler)

    return list(new_image.values()).count("#")


if __name__ == "__main__":
    challenge_input = get_input("aoc_2021/2021_20.txt")
    position_map, image = parse(challenge_input)
    print(enhance_and_count_lit_pixels(image, position_map, 50))
