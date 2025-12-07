from functools import reduce
import math
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


class maths:
    nums: list[int] = []
    symbol: str = None

    def doMath(self):
        if self.symbol == "+":
            return reduce(lambda x, y: x + y, self.nums)
        if self.symbol == "*":
            return reduce(lambda x, y: x * y, self.nums)


def solve_1(file_path):
    totals = []

    # create grid split each line white space
    with open(file_path, "r") as file:
        data = [line.strip().split() for line in file.readlines()]

    # Rotate to create expected format
    for row in zip(*data[::-1]):
        symbol = row[0]
        nums = row[1:]
        _m = maths()
        _m.nums = [int(num) for num in nums]
        _m.symbol = symbol
        totals.append(_m.doMath())

    return sum(totals)


def solve_2(file_path):
    # Keep white spaces
    grid = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            grid.append([c for c in line])

    # Rotate grid 90 degrees clockwise
    grid = [list(reversed(col)) for col in zip(*grid)]

    # Remove rows that are only whitespace
    grid = [row for row in grid if any(c.strip() for c in row)]

    totals = []

    # row[0] = symbol or blank (skip after symbol)
    math_list = []
    curr_symbol = None
    curr_nums = []
    for row in grid:
        # Handle first time symbol assignment
        if row[0].strip() != "" and curr_symbol is None:
            curr_symbol = row[0]
        elif row[0].strip() != "":
            app = maths()
            app.symbol = curr_symbol
            app.nums = curr_nums
            math_list.append(app)
            totals.append(app.doMath())
            curr_symbol = row[0]
            curr_nums = []
        curr_nums.append(int("".join(reversed(row[1:]))))
    # Append the last math
    app = maths()
    app.symbol = curr_symbol
    app.nums = curr_nums
    math_list.append(app)
    totals.append(app.doMath())

    return sum(totals)


def main():
    total = solve_1(INPUT_PATH)
    total_2 = solve_2(INPUT_PATH)
    print(f"Part 1: {total}")
    print(f"Part 2: {total_2}")


if __name__ == "__main__":
    main()
