import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


def read_input(file_path):
    with open(file_path, "r") as file:
        return file.readlines()[0].strip().split(",")


# part 1
def invalid_finder(start, end):
    invalid_ids = []
    for num in range(start, end + 1):
        str_num = str(num).lstrip("0")
        midpoint = len(str_num) // 2

        # Split the string into two halves
        first_half = str_num[:midpoint]
        second_half = str_num[midpoint:]

        if first_half == second_half:
            invalid_ids.append(num)

    return invalid_ids


# part 2
def pattern_finder(start, end):
    invalid_ids = []
    for num in range(start, end + 1):
        str_num = str(num).lstrip("0")
        match = re.fullmatch(r"(.+?)\1+$", str_num)
        if match:
            invalid_ids.append(num)
    return invalid_ids


def main():
    total_sum = 0
    p2_total_sum = 0
    input = read_input(INPUT_PATH)
    # Part 1
    for i in input:
        parts = i.split("-")
        start = int(parts[0])
        end = int(parts[1])
        invalids = invalid_finder(start, end)
        total_sum += sum(invalids)

    # Part 2
    for i in input:
        parts = i.split("-")
        start = int(parts[0])
        end = int(parts[1])
        invalids = pattern_finder(start, end)
        p2_total_sum += sum(invalids)

    print(f"Total sum of invalid IDs: {total_sum}")
    print(f"Total sum of invalid IDs - Part 2: {p2_total_sum}")


if __name__ == "__main__":
    main()
