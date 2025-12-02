"""
Day 2: Invalid Product ID Detection and Summation
Advent of Code 2025

This module identifies and sums invalid product IDs within specified ranges.
Invalid IDs are those formed by repeating digit sequences.
"""

import os
from typing import List, Tuple, Callable

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "input.txt")


def parse_input(text: str) -> List[Tuple[int, int]]:
    """
    Parse comma-separated ranges into list of (start, end) tuples.

    Handles multi-line input by joining lines and splitting on commas.
    Each range is formatted as "start-end" where both values are inclusive.

    Args:
        text: Input string containing comma-separated ranges (e.g., "11-22,95-115")

    Returns:
        List of tuples representing (start, end) ranges, inclusive

    Examples:
        >>> parse_input("11-22")
        [(11, 22)]
        >>> parse_input("11-22,95-115")
        [(11, 22), (95, 115)]
        >>> parse_input("11-22,\\n95-115")
        [(11, 22), (95, 115)]
    """
    # Join all lines and remove extra whitespace
    cleaned = text.replace("\n", "").strip()

    # Split on commas
    range_strings = cleaned.split(",")

    ranges = []
    for range_str in range_strings:
        range_str = range_str.strip()
        if not range_str:  # Skip empty strings
            continue

        # Parse "start-end" format
        parts = range_str.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid range format: {range_str}")

        start = int(parts[0].strip())
        end = int(parts[1].strip())

        if start <= 0 or end <= 0:
            raise ValueError(f"Range values must be positive: {range_str}")

        if start > end:
            raise ValueError(f"Range start must be <= end: {range_str}")

        ranges.append((start, end))

    return ranges


def is_invalid_part1(product_id: int) -> bool:
    """
    Check if a product ID is invalid under Part 1 rules.

    A product ID is invalid if it consists of a digit sequence repeated exactly twice.
    For example: 11 (1 repeated twice), 1010 (10 repeated twice), 123123 (123 repeated twice).

    Args:
        product_id: The product ID to check

    Returns:
        True if the ID is invalid (exact double repetition), False otherwise

    Examples:
        >>> is_invalid_part1(11)
        True
        >>> is_invalid_part1(1010)
        True
        >>> is_invalid_part1(123123)
        True
        >>> is_invalid_part1(101)
        False
        >>> is_invalid_part1(111)
        False
    """
    id_str = str(product_id)
    length = len(id_str)

    # Single digit cannot be invalid (need at least 2 digits for a pattern)
    if length < 2:
        return False

    # For exact double repetition, length must be even
    if length % 2 != 0:
        return False

    # Check if first half equals second half
    mid = length // 2
    first_half = id_str[:mid]
    second_half = id_str[mid:]

    return first_half == second_half


def is_invalid_part2(product_id: int) -> bool:
    """
    Check if a product ID is invalid under Part 2 rules.

    A product ID is invalid if it consists of a digit sequence repeated at least twice (2+).
    For example: 11 (1 repeated twice), 111 (1 repeated 3 times),
                 123123123 (123 repeated 3 times), 1212121212 (12 repeated 5 times).

    Args:
        product_id: The product ID to check

    Returns:
        True if the ID is invalid (2+ repetitions), False otherwise

    Examples:
        >>> is_invalid_part2(11)
        True
        >>> is_invalid_part2(111)
        True
        >>> is_invalid_part2(123123123)
        True
        >>> is_invalid_part2(101)
        False
    """
    id_str = str(product_id)
    length = len(id_str)

    # Single digit cannot be invalid (need at least 2 digits for a pattern)
    if length < 2:
        return False

    # Try each possible sequence length from 1 to length//2
    # (since we need at least 2 repetitions)
    for seq_length in range(1, length // 2 + 1):
        # Check if total length is divisible by sequence length
        if length % seq_length != 0:
            continue

        # Extract the candidate sequence
        sequence = id_str[:seq_length]

        # Check if the entire ID is this sequence repeated
        repetition_count = length // seq_length
        if repetition_count >= 2:
            # Verify by reconstructing
            if sequence * repetition_count == id_str:
                return True

    return False


def find_invalid_ids_in_range(
    start: int, end: int, validator: Callable[[int], bool]
) -> List[int]:
    """
    Find all invalid IDs within a given range using the provided validator function.

    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        validator: Function that returns True if an ID is invalid

    Returns:
        List of invalid product IDs found in the range

    Examples:
        >>> find_invalid_ids_in_range(11, 22, is_invalid_part1)
        [11, 22]
        >>> find_invalid_ids_in_range(95, 115, is_invalid_part1)
        [99]
    """
    invalid_ids = []
    for product_id in range(start, end + 1):
        if validator(product_id):
            invalid_ids.append(product_id)
    return invalid_ids


def calculate_invalid_sum(
    ranges: List[Tuple[int, int]], validator: Callable[[int], bool]
) -> int:
    """
    Calculate the sum of all invalid IDs across all ranges.

    Args:
        ranges: List of (start, end) tuples representing ID ranges
        validator: Function that returns True if an ID is invalid

    Returns:
        Sum of all invalid product IDs found

    Examples:
        >>> ranges = [(11, 22), (95, 115)]
        >>> calculate_invalid_sum(ranges, is_invalid_part1)
        132
    """
    total_sum = 0
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, validator)
        total_sum += sum(invalid_ids)
    return total_sum


def solve_part1(input_text: str) -> int:
    """
    Solve Part 1: Find sum of invalid IDs with exact double repetition.

    Args:
        input_text: Input string containing comma-separated ranges

    Returns:
        Sum of all invalid product IDs found
    """
    ranges = parse_input(input_text)
    return calculate_invalid_sum(ranges, is_invalid_part1)


def solve_part2(input_text: str) -> int:
    """
    Solve Part 2: Find sum of invalid IDs with 2+ repetitions.

    Args:
        input_text: Input string containing comma-separated ranges

    Returns:
        Sum of all invalid product IDs found
    """
    ranges = parse_input(input_text)
    return calculate_invalid_sum(ranges, is_invalid_part2)


def main():
    """Main entry point for Day 2 solution."""
    # Read input file
    with open(INPUT_PATH, "r") as f:
        input_text = f.read()

    # Solve both parts
    part1_answer = solve_part1(input_text)
    part2_answer = solve_part2(input_text)

    print(f"Part 1: {part1_answer}")
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
