"""
Safe Dial Password Calculator - Day 1 Advent of Code 2025

This module solves a safe-cracking puzzle where a password is derived
from tracking how many times a circular dial points at zero during a
sequence of rotations.

The solution supports two password methods:
- Standard: Count only when the dial ends at 0 after a rotation
- Click Method (0x434C49434B): Count every time the dial passes through 0

Key features:
- O(1) rotation simulation using modulo arithmetic
- O(n) overall complexity for n rotations
- Mathematical optimization to avoid iterating through individual clicks

Usage:
    python agent.py

This reads rotations from input.txt and outputs passwords for both methods.
"""

from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    """Rotation direction enumeration."""

    LEFT = "L"
    RIGHT = "R"


class Rotation(NamedTuple):
    """Represents a single rotation instruction."""

    direction: Direction
    distance: int


class PasswordMethod(Enum):
    """Password calculation method enumeration."""

    STANDARD = "standard"
    CLICK_METHOD = "0x434C49434B"


def parse_rotation(line: str) -> Rotation:
    """
    Parse a single rotation instruction from text.

    Args:
        line: String in format '[L|R][distance]' (e.g., 'L68', 'R1000')

    Returns:
        Rotation object with parsed direction and distance

    Raises:
        ValueError: If line format is invalid

    Examples:
        >>> parse_rotation('L68')
        Rotation(direction=Direction.LEFT, distance=68)
        >>> parse_rotation('R1000')
        Rotation(direction=Direction.RIGHT, distance=1000)
    """
    line = line.strip()
    if not line or len(line) < 2:
        raise ValueError(f"Invalid rotation format: '{line}'")

    direction_char = line[0].upper()
    distance_str = line[1:]

    if direction_char not in ("L", "R"):
        raise ValueError(f"Invalid direction: '{direction_char}'")

    try:
        distance = int(distance_str)
    except ValueError:
        raise ValueError(f"Invalid distance: '{distance_str}'")

    if distance < 0:
        raise ValueError(f"Distance must be non-negative: {distance}")

    direction = Direction.LEFT if direction_char == "L" else Direction.RIGHT
    return Rotation(direction=direction, distance=distance)


def parse_rotations(input_text: str) -> list[Rotation]:
    """
    Parse all rotation instructions from input text.

    Args:
        input_text: Multi-line string with one rotation per line

    Returns:
        List of parsed Rotation objects
    """
    rotations = []
    for line_num, line in enumerate(input_text.strip().split("\n"), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            rotations.append(parse_rotation(line))
        except ValueError as e:
            raise ValueError(f"Line {line_num}: {e}")
    return rotations


class RotationResult(NamedTuple):
    """Result of a rotation simulation."""

    final_position: int  # Position after rotation (0-99)
    zero_crossings: int  # Number of times dial pointed at 0


def calculate_zero_crossings(
    start_position: int, direction: Direction, distance: int, count_during: bool
) -> int:
    """
    Calculate number of zero crossings during a rotation using mathematics.

    This is an optimization to avoid iterating through each click.
    Time complexity: O(1) instead of O(distance)

    Args:
        start_position: Current dial position (0-99)
        direction: Rotation direction (LEFT or RIGHT)
        distance: Number of clicks to rotate
        count_during: If True, count zeros during rotation; if False, only count if ending at 0

    Returns:
        Number of times the dial pointed at 0

    Mathematical reasoning:
        - For RIGHT rotation: moving from p toward higher numbers
          Crossings = floor((p + d) / 100)
        - For LEFT rotation: moving from p toward lower numbers (wrapping)
          Crossings = ceil((d - p) / 100) if d > p else 0
          Or equivalently: (d + 99 - p) // 100

    Examples:
        >>> calculate_zero_crossings(50, Direction.RIGHT, 1000, True)
        10  # Crosses 0 ten times
        >>> calculate_zero_crossings(50, Direction.RIGHT, 1000, False)
        1   # Ends at 50, not 0
        >>> calculate_zero_crossings(52, Direction.LEFT, 48, True)
        0   # Goes from 52 to 4, no crossings
        >>> calculate_zero_crossings(52, Direction.LEFT, 52, True)
        1   # Ends at 0 (52-52=0, crosses once)
    """
    if distance == 0:
        return 0

    if not count_during:
        # Only count if we end exactly at 0
        final_position = (
            start_position + (distance if direction == Direction.RIGHT else -distance)
        ) % 100
        return 1 if final_position == 0 else 0

    # Count all crossings during rotation
    # Key insight: count how many times we land on position 0 after each click
    #
    if direction == Direction.RIGHT:
        # Moving from start_position, we visit: start+1, start+2, ..., start+distance
        # We land on 0 when (start + k) ≡ 0 (mod 100) for k in [1, distance]
        # This is equivalent to: start + k = 100m for some positive integer m
        # Number of multiples of 100 in range (start, start+distance]
        crossings = (start_position + distance) // 100 - start_position // 100
    else:
        # Moving LEFT from start_position, we visit: start-1, start-2, ..., start-distance
        # We land on 0 when (start - k) ≡ 0 (mod 100) for k in [1, distance]
        # This means start = k (mod 100)

        if start_position == 0:
            # Special case: starting at 0, we move to 99, 98, ...
            # We don't hit 0 until we've gone 100, 200, etc. clicks
            crossings = distance // 100
        elif distance < start_position:
            crossings = 0
        else:
            # We hit 0 for the first time after start_position clicks
            # Then every 100 more clicks
            remaining = distance - start_position
            crossings = 1 + remaining // 100

    return crossings


def simulate_rotation(
    start_position: int, rotation: Rotation, count_during: bool
) -> RotationResult:
    """
    Simulate a single rotation on the dial.

    Args:
        start_position: Current dial position (0-99)
        rotation: Rotation instruction to execute
        count_during: If True, count zeros during rotation; if False, only count if ending at 0

    Returns:
        RotationResult with final position and zero crossing count

    Examples:
        >>> simulate_rotation(50, Rotation(Direction.RIGHT, 1000), True)
        RotationResult(final_position=50, zero_crossings=10)
        >>> simulate_rotation(50, Rotation(Direction.LEFT, 68), True)
        RotationResult(final_position=82, zero_crossings=1)
        >>> simulate_rotation(50, Rotation(Direction.LEFT, 68), False)
        RotationResult(final_position=82, zero_crossings=0)
    """
    # Calculate final position
    if rotation.direction == Direction.RIGHT:
        final_position = (start_position + rotation.distance) % 100
    else:
        final_position = (start_position - rotation.distance) % 100

    # Calculate zero crossings
    zero_crossings = calculate_zero_crossings(
        start_position, rotation.direction, rotation.distance, count_during
    )

    return RotationResult(final_position=final_position, zero_crossings=zero_crossings)


def calculate_password(rotations: list[Rotation], method: PasswordMethod) -> int:
    """
    Calculate the safe password by executing rotations and counting zero crossings.

    Args:
        rotations: List of rotation instructions to execute
        method: Password calculation method (STANDARD or CLICK_METHOD)

    Returns:
        The calculated password (total zero crossings)

    The dial starts at position 50 and processes each rotation sequentially.

    Password methods:
    - STANDARD: Count only when dial ends at 0 after a rotation
    - CLICK_METHOD: Count every time dial passes through 0 (including during rotation)

    Examples:
        >>> rotations = [
        ...     Rotation(Direction.LEFT, 68),
        ...     Rotation(Direction.LEFT, 30),
        ...     Rotation(Direction.RIGHT, 48)
        ... ]
        >>> calculate_password(rotations, PasswordMethod.STANDARD)
        1
        >>> calculate_password(rotations, PasswordMethod.CLICK_METHOD)
        3
    """
    current_position = 50  # Starting position
    total_zero_crossings = 0
    count_during = method == PasswordMethod.CLICK_METHOD

    for rotation in rotations:
        result = simulate_rotation(current_position, rotation, count_during)
        total_zero_crossings += result.zero_crossings
        current_position = result.final_position

    return total_zero_crossings


def solve_part1(input_text: str) -> int:
    """
    Solve Part 1: Calculate password using Standard method.

    Args:
        input_text: Multi-line string with rotation instructions

    Returns:
        Password calculated using Standard method (count only when ending at 0)
    """
    rotations = parse_rotations(input_text)
    return calculate_password(rotations, PasswordMethod.STANDARD)


def solve_part2(input_text: str) -> int:
    """
    Solve Part 2: Calculate password using Click Method.

    Args:
        input_text: Multi-line string with rotation instructions

    Returns:
        Password calculated using Click Method (count all zero crossings)
    """
    rotations = parse_rotations(input_text)
    return calculate_password(rotations, PasswordMethod.CLICK_METHOD)


def read_input_file(filepath: str = "input.txt") -> str:
    """
    Read puzzle input from file.

    Args:
        filepath: Path to input file (default: "input.txt")

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    with open(filepath, "r") as f:
        return f.read()


def main() -> int:
    """
    Main entry point for the safe dial password calculator.

    Reads rotations from input.txt and calculates passwords for both methods.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Read input
        input_text = read_input_file()

        # Calculate passwords
        part1_answer = solve_part1(input_text)
        part2_answer = solve_part2(input_text)

        # Output results
        print(f"Part 1 (Standard Method): {part1_answer}")
        print(f"Part 2 (Click Method 0x434C49434B): {part2_answer}")

        return 0

    except FileNotFoundError:
        print("Error: input.txt not found")
        return 1
    except ValueError as e:
        print(f"Error parsing input: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
