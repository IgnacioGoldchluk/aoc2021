# target area: x=150..193, y=-136..-86
# max_y_height = sum(range(1, abs(min_y_point)))
import itertools

candidate_speeds = itertools.product(range(17, 194), range(-136, 136))

target_grid = ((150, -86), (193, -136))


def out_of_bounds(position, target_grid):
    return position[1] < target_grid[1][1]


def position_in_grid(position, target_grid):
    x_in_grid = target_grid[0][0] <= position[0] <= target_grid[1][0]
    y_in_grid = target_grid[1][1] <= position[1] <= target_grid[0][1]
    return x_in_grid and y_in_grid


def update_position(position, speed):
    return [position[0] + speed[0], position[1] + speed[1]]


def update_speed(speed):
    return [max(speed[0] - 1, 0), speed[1] - 1]


valid_points = 0
for speed in candidate_speeds:
    position = [0, 0]
    while not out_of_bounds(position, target_grid):
        if position_in_grid(position, target_grid):
            valid_points += 1
            break
        position = update_position(position, speed)
        speed = update_speed(speed)
print(valid_points)
