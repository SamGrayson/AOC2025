import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


def read_input(file_path):
    ranges, ingredients = set(), set()
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if "" == line:
                continue
            if "-" in line:
                bounds = line.split("-")
                ranges.add((int(bounds[0]), int(bounds[1])))
            else:
                ingredients.add(int(line))

    ranges = sorted(ranges, key=lambda x: x[0])

    return ranges, ingredients


def all_fresh(ranges):
    fresh_count = 0
    start = None
    end = None
    for i, r in enumerate(ranges):
        if i == len(ranges) - 1:
            if r[0] <= end <= r[1]:
                fresh_count += r[1] - start + 1
            else:
                fresh_count += end - start + 1
                fresh_count += r[1] - r[0] + 1
            break

        if start is None:
            start = r[0]
            end = r[1]
        else:
            if r[0] <= end <= r[1]:
                # Overlap - extend the range
                end = r[1]
            elif end >= r[1]:
                # Fully contained - do nothing
                continue
            else:
                fresh_count += end - start + 1
                start = r[0]
                end = r[1]
    return fresh_count


def main():
    ranges, ingredients = read_input(INPUT_PATH)
    fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                fresh += 1
                break
    total_fresh = all_fresh(ranges)
    print(f"Part 1: {fresh}")
    print(f"Part 2: {total_fresh}")


if __name__ == "__main__":
    main()
