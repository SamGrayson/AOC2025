import math
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


def read_input(file_path):
    coords = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            x_str, y_str, z_str = line.strip().split(",")
            coords.append((int(x_str), int(y_str), int(z_str)))
    return coords


def euclidean_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def p1(distances, iter=10, total_coords=None):
    connections = {}
    last_connection = None
    group_id = 1

    for i, ((a, b), _) in enumerate(distances):
        if i >= iter:
            break

        # Both already connected
        if a in connections and b in connections:
            # If in different groups, merge them
            if connections[a] != connections[b]:
                old_group = connections[b]
                new_group = connections[a]
                for node in connections:
                    if connections[node] == old_group:
                        connections[node] = new_group
            continue
        # No connections yet
        elif a not in connections and b not in connections:
            connections[a] = group_id
            connections[b] = group_id
            group_id += 1
        # If connection exists for a or b, assign the same group id
        elif a in connections:
            connections[b] = connections[a]
        elif b in connections:
            connections[a] = connections[b]

        # Check if all coords are in one group (loop)
        if (
            total_coords
            and len(connections) == total_coords
            and len(set(connections.values())) == 1
        ):
            last_connection = (a, b)
            break

    groups = {}
    for gid in connections.values():
        groups[gid] = groups.get(gid, 0) + 1

    return math.prod(sorted(list(groups.values()), reverse=True)[:3]), last_connection


def main():
    coords = read_input(INPUT_PATH)
    distances = set()
    for a in coords:
        for b in coords:
            if a == b:
                continue
            d = euclidean_distance(a, b)
            # Remove duplicate tuples
            if ((b, a), d) not in distances:
                distances.add(((a, b), d))

    sorted_distances = sorted(distances, key=lambda item: item[1])
    result, last_connection = p1(sorted_distances, math.inf, len(coords))

    print("Part 1:", result)
    print("Part 2:", last_connection[0][0] * last_connection[1][0])


if __name__ == "__main__":

    main()
