from functools import lru_cache
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")

dirs = {
    "d": (1, 0),
    "r": (0, 1),
    "l": (0, -1),
    "u": (-1, 0),
}


def solve_1(file_path):
    # create grid split from file
    grid = {}
    start_pos: tuple[int, int]
    grid_len: int
    row_len: int

    with open(file_path, "r") as file:
        grid_len = len(file.readlines()) - 1
        file.seek(0)
        for y, line in enumerate(file.readlines()):
            row_len = len(line.strip())
            for x, c in enumerate(line.strip()):
                if c == "S":
                    start_pos = (y, x)
                grid[(y, x)] = c

    cache = set()
    totals = {
        "split_count": 0,
    }

    def traverse(pos):
        if pos in cache:
            return
        cache.add(pos)
        y, x = pos
        # If past the boundary, stop
        if y + dirs["d"][0] > grid_len:
            return
        ny = y + dirs["d"][0]
        nx = x + dirs["d"][1]
        next = grid.get((ny, nx))
        if next == "^":
            totals["split_count"] += 1
            # Left
            if 0 <= nx + dirs["l"][1] <= row_len:
                traverse((ny, nx + dirs["l"][1]))
            # Right
            if 0 <= nx + dirs["r"][1] <= row_len:
                traverse((ny, nx + dirs["r"][1]))

        elif next == ".":
            traverse((ny, nx))
        return

    traverse(start_pos)
    return totals["split_count"]


def solve_2(file_path):
    # create grid split from file
    grid = {}
    start_pos: tuple[int, int]
    grid_len: int
    row_len: int

    with open(file_path, "r") as file:
        grid_len = len(file.readlines()) - 1
        file.seek(0)
        for y, line in enumerate(file.readlines()):
            row_len = len(line.strip())
            for x, c in enumerate(line.strip()):
                if c == "S":
                    start_pos = (y, x)
                grid[(y, x)] = c

    @lru_cache(maxsize=None)
    def traverse(pos, prev_pos):
        y, x = pos
        # If past the boundary, we reached an end
        if y + dirs["d"][0] > grid_len:
            return 1

        ny = y + dirs["d"][0]
        nx = x + dirs["d"][1]
        next = grid.get((ny, nx))

        total = 0
        if next == "^":
            # Left
            if 0 <= nx + dirs["l"][1] <= row_len:
                total += traverse((ny, nx + dirs["l"][1]), pos)
            # Right
            if 0 <= nx + dirs["r"][1] <= row_len:
                total += traverse((ny, nx + dirs["r"][1]), pos)
        elif next == ".":
            total += traverse((ny, nx), pos)

        return total

    unique_paths = traverse(start_pos, None)

    return unique_paths


def main():
    split_count = solve_1(INPUT_PATH)
    paths_count = solve_2(INPUT_PATH)
    print(f"Part 1: {split_count}")
    print(f"Part 2: {paths_count}")


if __name__ == "__main__":
    main()
