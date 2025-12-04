import os

from sqlalchemy import true

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


grid_map = {}

# Excluding self / center square
square = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]


def read_input(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def roll_access(grid_map):
    rolls_for_deletion = {}
    for key, value in grid_map.items():
        if value != "@":
            continue
        y, x = key
        at_count = 0
        for dy, dx in square:
            ny, nx = y + dy, x + dx
            if (ny, nx) in grid_map and grid_map[(ny, nx)] == "@":
                at_count += 1
            if at_count >= 4:
                break
        if at_count < 4:
            rolls_for_deletion[key] = "."
    return rolls_for_deletion


def main():
    input_lines = read_input(INPUT_PATH)
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            grid_map[(y, x)] = char

    p1_rolls = len(roll_access(grid_map))

    print(f"Part 1: {p1_rolls}")

    # Loop until no more rolls can be made
    total_rolls = 0
    while True:
        rolls = roll_access(grid_map)
        if len(rolls) == 0:
            break
        else:
            total_rolls += len(rolls)
            grid_map.update(rolls)

    print(f"Part 2: {total_rolls}")


if __name__ == "__main__":
    main()
