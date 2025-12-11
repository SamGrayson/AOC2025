import math
import os
from shapely.geometry import Polygon, box
from shapely.prepared import prep

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")

max_ydir = 0
max_xdir = 0
min_ydir = math.inf
min_xdir = math.inf


def read_input(file_path):
    coords = []
    for line in open(file_path, "r"):
        x_str, y_str = line.strip().split(",")
        coords.append((int(x_str), int(y_str)))
        global max_ydir, max_xdir, min_ydir, min_xdir
        if int(y_str) > max_ydir:
            max_ydir = int(y_str)
        if int(x_str) > max_xdir:
            max_xdir = int(x_str)
        if int(y_str) < min_ydir:
            min_ydir = int(y_str)
        if int(x_str) < min_xdir:
            min_xdir = int(x_str)
    return coords


# This needs to be y,x distance like in a grid
def man_distance(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (abs(a[0] - b[0]) + 1, abs(a[1] - b[1]) + 1)


def create_polygon_boundary(coords):
    boundary = []

    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        dy = y2 - y1
        dx = x2 - x1
        steps = max(abs(dy), abs(dx))

        if steps == 0:
            boundary.append((x1, y1))  # Keep as (x, y)
        else:
            for step in range(steps + 1):
                y = y1 + (dy * step) // steps
                x = x1 + (dx * step) // steps
                boundary.append((x, y))  # Keep as (x, y)

    return boundary


def p2(boundary, distances):
    polygon = Polygon(boundary)
    prepared_polygon = prep(polygon)  # Much faster for repeated containment checks

    for (a, b), d, area in sorted(distances, key=lambda x: x[2], reverse=True):
        # a and b are (x, y) tuples
        rect = box(
            min(a[0], b[0]),  # min x
            min(a[1], b[1]),  # min y
            max(a[0], b[0]),  # max x
            max(a[1], b[1]),  # max y
        )
        if prepared_polygon.contains(rect):
            return area

    return None


def main():
    coords = read_input(INPUT_PATH)
    distances = set()
    max_area = 0
    for a in coords:
        for b in coords:
            if a == b:
                continue
            d = man_distance(a, b)
            area = d[0] * d[1]
            if area > max_area:
                max_area = area
            # Remove duplicate tuples
            if ((b, a), d, area) not in distances:
                distances.add(((a, b), d, area))
    print("Part 1:", max_area)

    boundary = create_polygon_boundary(coords)

    grid = p2(boundary, distances)

    print("Part 2:", grid)


if __name__ == "__main__":
    main()
