import os
from py_compile import main

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")

nums = [n for n in range(0, 100)]


def read_input(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


# Part 1
def calculate_turn_idx(current_value, dir, distance):
    if dir == "L":
        for _ in range(distance):
            current_value -= 1
            if current_value < 0:
                current_value = 99
        return current_value
    elif dir == "R":
        for _ in range(distance):
            current_value += 1
            if current_value > 99:
                current_value = 0
        return current_value


# Part 2
def calculate_turn_zero_count(current_value, dir, distance):
    count = 0
    if dir == "L":
        for _ in range(distance):
            current_value -= 1
            # Click goes to 0, so check before
            if current_value == 0:
                count += 1
            if current_value < 0:
                current_value = 99
        return current_value, count
    elif dir == "R":
        for _ in range(distance):
            current_value += 1
            if current_value > 99:
                current_value = 0
            # Click goes to 100, so check after
            if current_value == 0:
                count += 1
        return current_value, count


def main_1():
    lines = read_input(INPUT_PATH)
    count = 0
    curr = 50
    for line in lines:
        dir = line[0]
        distance = int(line[1:])
        curr = calculate_turn_idx(curr, dir, distance)
        if curr == 0:
            count += 1
    print(f"Number of times landed on 0: {count}")


def main_2():
    lines = read_input(INPUT_PATH)
    zero_count = 0
    curr = 50
    for line in lines:
        dir = line[0]
        distance = int(line[1:])
        curr, _zero_count = calculate_turn_zero_count(curr, dir, distance)
        zero_count += _zero_count
    print(f"Number of times clicked to 0: {zero_count}")


if __name__ == "__main__":
    main_1()
    main_2()
