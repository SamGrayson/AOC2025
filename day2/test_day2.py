"""
Tests for Day 2: Invalid Product ID Detection and Summation
"""

import unittest
from agent import (
    parse_input,
    is_invalid_part1,
    is_invalid_part2,
    find_invalid_ids_in_range,
    calculate_invalid_sum,
    solve_part1,
    solve_part2,
)


# Example input from specification
EXAMPLE_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

PART1_EXPECTED_SUM = 1227775554
PART2_EXPECTED_SUM = 4174379265


class TestInputParsing(unittest.TestCase):
    """Tests for input parsing functionality."""

    def test_parse_single_range(self):
        """Test parsing a single range."""
        result = parse_input("11-22")
        self.assertEqual(result, [(11, 22)])

    def test_parse_multiple_ranges(self):
        """Test parsing multiple comma-separated ranges."""
        result = parse_input("11-22,95-115")
        self.assertEqual(result, [(11, 22), (95, 115)])

    def test_parse_multiline_input(self):
        """Test parsing input that spans multiple lines."""
        result = parse_input("11-22,95-115,\n998-1012")
        self.assertEqual(result, [(11, 22), (95, 115), (998, 1012)])

    def test_parse_example_input(self):
        """Test parsing the complete example input."""
        result = parse_input(EXAMPLE_INPUT)
        expected = [
            (11, 22),
            (95, 115),
            (998, 1012),
            (1188511880, 1188511890),
            (222220, 222224),
            (1698522, 1698528),
            (446443, 446449),
            (38593856, 38593862),
            (565653, 565659),
            (824824821, 824824827),
            (2121212118, 2121212124),
        ]
        self.assertEqual(result, expected)

    def test_parse_handles_whitespace(self):
        """Test that parser handles extra whitespace."""
        result = parse_input(" 11-22 , 95-115 ")
        self.assertEqual(result, [(11, 22), (95, 115)])


class TestPatternDetectionPart1(unittest.TestCase):
    """Tests for Part 1 pattern detection (exact double repetition)."""

    def test_invalid_two_digit_same(self):
        """Test that 11, 22, etc. are invalid (single digit repeated twice)."""
        self.assertTrue(is_invalid_part1(11))
        self.assertTrue(is_invalid_part1(22))
        self.assertTrue(is_invalid_part1(99))

    def test_invalid_four_digit_pattern(self):
        """Test that 1010, 6464, etc. are invalid (two digits repeated twice)."""
        self.assertTrue(is_invalid_part1(1010))
        self.assertTrue(is_invalid_part1(6464))

    def test_invalid_six_digit_pattern(self):
        """Test that 123123 is invalid (three digits repeated twice)."""
        self.assertTrue(is_invalid_part1(123123))

    def test_invalid_large_pattern(self):
        """Test large patterns like 1188511885, 222222, 446446, 38593859."""
        self.assertTrue(is_invalid_part1(1188511885))
        self.assertTrue(is_invalid_part1(222222))
        self.assertTrue(is_invalid_part1(446446))
        self.assertTrue(is_invalid_part1(38593859))

    def test_valid_single_digit(self):
        """Test that single-digit numbers are valid (cannot be exact double)."""
        self.assertFalse(is_invalid_part1(1))
        self.assertFalse(is_invalid_part1(5))
        self.assertFalse(is_invalid_part1(9))

    def test_valid_three_digit_no_pattern(self):
        """Test that 101, 111 are valid (111 is triple, not double)."""
        self.assertFalse(is_invalid_part1(101))
        self.assertFalse(is_invalid_part1(111))  # Triple repetition, not double

    def test_valid_no_pattern(self):
        """Test numbers with no repetition pattern."""
        self.assertFalse(is_invalid_part1(123))
        self.assertFalse(is_invalid_part1(1234))
        self.assertFalse(is_invalid_part1(99999))  # 5 repetitions, not 2


class TestRangeProcessingPart1(unittest.TestCase):
    """Tests for Part 1 range processing."""

    def test_range_11_22(self):
        """Test range 11-22 finds invalid IDs 11 and 22."""
        result = find_invalid_ids_in_range(11, 22, is_invalid_part1)
        self.assertEqual(result, [11, 22])

    def test_range_95_115(self):
        """Test range 95-115 finds invalid ID 99."""
        result = find_invalid_ids_in_range(95, 115, is_invalid_part1)
        self.assertEqual(result, [99])

    def test_range_998_1012(self):
        """Test range 998-1012 finds invalid ID 1010."""
        result = find_invalid_ids_in_range(998, 1012, is_invalid_part1)
        self.assertEqual(result, [1010])

    def test_range_no_invalid_ids(self):
        """Test range with no invalid IDs returns empty list."""
        result = find_invalid_ids_in_range(1698522, 1698528, is_invalid_part1)
        self.assertEqual(result, [])

    def test_single_element_range_invalid(self):
        """Test single-element range with invalid ID."""
        result = find_invalid_ids_in_range(11, 11, is_invalid_part1)
        self.assertEqual(result, [11])

    def test_single_element_range_valid(self):
        """Test single-element range with valid ID."""
        result = find_invalid_ids_in_range(12, 12, is_invalid_part1)
        self.assertEqual(result, [])


class TestPart1Integration(unittest.TestCase):
    """Integration tests for Part 1 complete solution."""

    def test_calculate_sum_example_ranges(self):
        """Test sum calculation with example ranges."""
        ranges = [
            (11, 22),
            (95, 115),
            (998, 1012),
        ]
        result = calculate_invalid_sum(ranges, is_invalid_part1)
        # 11 + 22 + 99 + 1010 = 1142
        self.assertEqual(result, 1142)

    def test_calculate_sum_no_invalid(self):
        """Test sum when no invalid IDs exist."""
        ranges = [(1698522, 1698528)]
        result = calculate_invalid_sum(ranges, is_invalid_part1)
        self.assertEqual(result, 0)

    def test_calculate_sum_empty_ranges(self):
        """Test sum with empty range list."""
        result = calculate_invalid_sum([], is_invalid_part1)
        self.assertEqual(result, 0)

    def test_complete_example_part1(self):
        """Test complete example input produces expected Part 1 sum."""
        ranges = parse_input(EXAMPLE_INPUT)
        result = calculate_invalid_sum(ranges, is_invalid_part1)
        self.assertEqual(result, PART1_EXPECTED_SUM)


class TestPatternDetectionPart2(unittest.TestCase):
    """Tests for Part 2 pattern detection (2+ repetitions)."""

    def test_all_part1_invalid_still_invalid(self):
        """Test that all Part 1 invalid IDs remain invalid in Part 2."""
        part1_invalid = [
            11,
            22,
            99,
            1010,
            6464,
            123123,
            1188511885,
            222222,
            446446,
            38593859,
        ]
        for product_id in part1_invalid:
            with self.subTest(product_id=product_id):
                self.assertTrue(is_invalid_part2(product_id))

    def test_invalid_triple_repetition(self):
        """Test that triple repetitions are invalid in Part 2."""
        self.assertTrue(is_invalid_part2(111))  # "1" repeated 3 times
        self.assertTrue(is_invalid_part2(999))  # "9" repeated 3 times
        self.assertTrue(is_invalid_part2(123123123))  # "123" repeated 3 times

    def test_invalid_multiple_repetitions(self):
        """Test patterns with 4+ repetitions."""
        self.assertTrue(is_invalid_part2(1212121212))  # "12" repeated 5 times
        self.assertTrue(is_invalid_part2(1111111))  # "1" repeated 7 times
        self.assertTrue(is_invalid_part2(565656))  # "56" repeated 3 times
        self.assertTrue(is_invalid_part2(824824824))  # "824" repeated 3 times
        self.assertTrue(is_invalid_part2(2121212121))  # "21" repeated 5 times

    def test_valid_no_repetition(self):
        """Test that IDs without repetition patterns are valid."""
        self.assertFalse(is_invalid_part2(101))
        self.assertFalse(is_invalid_part2(123))
        self.assertFalse(is_invalid_part2(1234))

    def test_valid_single_digit(self):
        """Test that single digits are valid."""
        self.assertFalse(is_invalid_part2(1))
        self.assertFalse(is_invalid_part2(9))


class TestPart2Integration(unittest.TestCase):
    """Integration tests for Part 2 complete solution."""

    def test_range_95_115_part2(self):
        """Test range 95-115 finds both 99 and 111 in Part 2."""
        result = find_invalid_ids_in_range(95, 115, is_invalid_part2)
        self.assertIn(99, result)
        self.assertIn(111, result)

    def test_range_998_1012_part2(self):
        """Test range 998-1012 finds both 999 and 1010 in Part 2."""
        result = find_invalid_ids_in_range(998, 1012, is_invalid_part2)
        self.assertIn(999, result)
        self.assertIn(1010, result)

    def test_range_565653_565659_part2(self):
        """Test range 565653-565659 finds 565656 in Part 2."""
        result = find_invalid_ids_in_range(565653, 565659, is_invalid_part2)
        self.assertEqual(result, [565656])

    def test_range_824824821_824824827_part2(self):
        """Test range 824824821-824824827 finds 824824824 in Part 2."""
        result = find_invalid_ids_in_range(824824821, 824824827, is_invalid_part2)
        self.assertEqual(result, [824824824])

    def test_range_2121212118_2121212124_part2(self):
        """Test range 2121212118-2121212124 finds 2121212121 in Part 2."""
        result = find_invalid_ids_in_range(2121212118, 2121212124, is_invalid_part2)
        self.assertEqual(result, [2121212121])

    def test_complete_example_part2(self):
        """Test complete example input produces expected Part 2 sum."""
        ranges = parse_input(EXAMPLE_INPUT)
        result = calculate_invalid_sum(ranges, is_invalid_part2)
        self.assertEqual(result, PART2_EXPECTED_SUM)


class TestSolutionFunctions(unittest.TestCase):
    """Tests for high-level solution functions."""

    def test_solve_part1_with_example(self):
        """Test solve_part1 with example input."""
        result = solve_part1(EXAMPLE_INPUT)
        self.assertEqual(result, PART1_EXPECTED_SUM)

    def test_solve_part2_with_example(self):
        """Test solve_part2 with example input."""
        result = solve_part2(EXAMPLE_INPUT)
        self.assertEqual(result, PART2_EXPECTED_SUM)


if __name__ == "__main__":
    unittest.main()
