from collections import deque
import os
from time import time
from z3 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


# Format input: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
def read_input(file_path) -> list[tuple[list[int], list[list[int]], list[int]]]:
    steps = []
    for line in open(file_path, "r"):
        stuff = line.strip().split(" ")
        light = []
        for c in stuff[0]:
            if c == "[" or c == "]":
                continue
            light.append(c)
        buttons = []
        voltage = set()
        for b in stuff[1:]:
            if b.startswith("("):
                _b = [int(x) for x in b.strip("()").split(",")]
                buttons.append(_b)
            elif b.startswith("{"):
                voltage = [int(n) for n in b.strip("{}").split(",")]
        steps.append((light, buttons, voltage))
    return steps


def press_button(curr_light: list[int], button: list[int]):
    next_light = curr_light.copy()

    for idx in button:
        if next_light[idx] == "#":
            next_light[idx] = "."
        else:
            next_light[idx] = "#"

    return next_light


def voltage_too_high(curr_voltage, target_voltage):
    for cv, tv in zip(curr_voltage, target_voltage):
        if cv > tv:
            return True
    return False


# Attempt to uze z3
def p2(steps):
    # Example (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    # buttons 1, 2, 3, 4, 5, 6
    # 1: int('5') + int('6') = 3
    # 2:
    # opt = Optimize()
    # b1 = Int("b1")
    # b2 = Int("b2")
    # b3 = Int("b3")
    # b4 = Int("b4")
    # b5 = Int("b5")
    # b6 = Int("b6")
    # opt.add(b1 >= 0)
    # opt.add(b2 >= 0)
    # opt.add(b3 >= 0)
    # opt.add(b4 >= 0)
    # opt.add(b5 >= 0)
    # opt.add(b6 >= 0)
    # opt.add(Sum([b5, b6]) == 3)
    # opt.add(Sum([b2, b6]) == 5)
    # opt.add(Sum([b3, b4, b5]) == 4)
    # opt.add(Sum([b1, b2, b4]) == 7)
    # print(opt.check())
    # m = opt.model()
    # print(m.eval(b1))
    # print(m.eval(b2))
    # print(m.eval(b3))
    # print(m.eval(b4))
    # print(m.eval(b5))
    # print(m.eval(b6))

    min_presses = []

    for _, buttons, target_voltage in steps:
        opt = Optimize()
        ints = []
        # Add "int" - like x - for each button
        for b in range(1, len(buttons) + 1):
            ints.append(Int(f"b{b}"))
        # Buttons must be greater than 0
        for i in ints:
            opt.add(i >= 0)
        # Take each button and see if they add to the voltage index
        for i, amount in enumerate(target_voltage):
            ints_for_i = []
            for bidx, b in enumerate(buttons):
                if i in b:
                    ints_for_i.append(ints[bidx])
            opt.add(Sum(ints_for_i) == amount)

        # Minimize the total number of button presses - WOW REQUIRED
        opt.minimize(Sum(ints))

        opt.check()
        m = opt.model()
        # sum the results of m
        presses = []
        for i in ints:
            val = m.eval(i)
            presses.append(val.as_long())
        min_presses.append(sum(presses))
    return sum(min_presses)


# Lights
def p1(steps):
    min_presses = []

    for light, buttons, _ in steps:
        queue = deque((["." for _ in light], b, 0) for b in buttons)
        visited = set()
        while queue:
            curr_light, b, presses = queue.popleft()
            if (tuple(curr_light), presses, tuple(b)) in visited:
                continue
            visited.add((tuple(curr_light), presses, tuple(b)))

            for b in buttons:
                next_light = press_button(curr_light, b)
                if next_light == light:
                    min_presses.append(presses + 1)
                    queue.clear()
                    break
                queue.append((next_light, b, presses + 1))

    return sum(min_presses)


def main():
    steps = read_input(INPUT_PATH)

    p1_res = p1(steps)

    print("Part 1:", p1_res)

    p2_res = p2(steps)

    print("Part 2:", p2_res)


if __name__ == "__main__":
    main()
