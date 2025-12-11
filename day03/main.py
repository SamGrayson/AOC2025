import itertools
import os
from typing import final

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


def read_input(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def largest_2_volts(bank):
    nums = [int(n) for n in bank]
    possibles = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            possibles.append(int(f"{nums[i]}{nums[j]}"))
    return max(possibles)


# Original recursive solution for part 2
def largest_12_volts(bank):
    nums = [n for n in bank]
    mem = set()
    possibles = list(range(0, 10))
    possibles.reverse()
    maxes = []
    max_idx = {}

    def recursor(current_str, idx):
        # If we're going down a less path than a found max - stop
        if int(current_str) <= max_idx.get(len(current_str), -1):
            return

        if int(current_str) in mem:
            return

        if len(current_str) == 12:
            mem.add(int(current_str))
            maxes.append(int(current_str))

            # take each chunked number and add it to the max idx so that we don't go down any rabit holes
            for i in range(len(current_str), -1, -1):
                if current_str[:i]:
                    num = int(current_str[:i])
                    max_idx[i] = num

            return

        for j in range(idx, len(nums)):
            recursor(current_str + nums[j], j + 1)

    for p in possibles:
        indexes = [i for i, n in enumerate(nums) if int(n) == p]
        for idx in indexes:
            recursor(nums[idx], idx + 1)
        if len(maxes) > 0:
            break

    return max(maxes)


# A much more efficient way to do part 2 - rewritten below
def largest_12_volts_grouped(current_str, required=12):
    """
    1. Take each digit and store its index and value as a tuple in a list.
    2. Sort the list from largest value to smallest.
    3. Look at each sorted pair and make sure it can be added to the current number by comparing what digits & their index have already been used and the remaining digits in the string.
    """
    ordered_bank = []
    for i, n in enumerate(current_str):
        ordered_bank.append((i, int(n)))
    # Sort from largest value to smallest value
    ordered_bank = sorted(ordered_bank, key=lambda x: x[1], reverse=True)
    joltage = []
    previous_index = -1
    for digit_index in range(required):
        for i, d in enumerate(ordered_bank):
            # Farthest index we can use for this digit
            max_index = len(current_str) - required + digit_index + 1
            # If this digit's index is valid to use - continue
            if previous_index < d[0] < max_index:
                joltage.append(d[1])
                previous_index = d[0]
                ordered_bank = ordered_bank[:i] + ordered_bank[i + 1 :]
                break
    return int("".join(map(str, joltage)))


def main():
    p1_total = 0
    p2_total = 0
    lines = read_input(INPUT_PATH)
    for line in lines:
        res = largest_2_volts(line)
        p1_total += res
    for line in lines:
        res = largest_12_volts_grouped(line)
        print(f"Line: {line} -> {res}")
        p2_total += res

    print(f"Part 1: {p1_total}")
    print(f"Part 2: {p2_total}")


if __name__ == "__main__":
    main()
