import unittest
from agent import (
    parse_rotation,
    parse_rotations,
    Direction,
    Rotation,
    simulate_rotation,
    calculate_zero_crossings,
    RotationResult,
    calculate_password,
    solve_part1,
    solve_part2,
    PasswordMethod,
)


class TestRotationParsing(unittest.TestCase):
    """Test rotation instruction parsing."""

    def test_parse_left_rotation(self):
        result = parse_rotation("L68")
        self.assertEqual(result.direction, Direction.LEFT)
        self.assertEqual(result.distance, 68)

    def test_parse_right_rotation(self):
        result = parse_rotation("R1000")
        self.assertEqual(result.direction, Direction.RIGHT)
        self.assertEqual(result.distance, 1000)

    def test_parse_zero_distance(self):
        result = parse_rotation("L0")
        self.assertEqual(result.distance, 0)

    def test_parse_with_whitespace(self):
        result = parse_rotation("  R48  ")
        self.assertEqual(result.direction, Direction.RIGHT)
        self.assertEqual(result.distance, 48)

    def test_parse_invalid_direction(self):
        with self.assertRaises(ValueError):
            parse_rotation("X100")

    def test_parse_invalid_distance(self):
        with self.assertRaises(ValueError):
            parse_rotation("Labc")

    def test_parse_empty_string(self):
        with self.assertRaises(ValueError):
            parse_rotation("")

    def test_parse_multiple_rotations(self):
        input_text = "L68\nR48\nL30"
        rotations = parse_rotations(input_text)
        self.assertEqual(len(rotations), 3)
        self.assertEqual(rotations[0].direction, Direction.LEFT)
        self.assertEqual(rotations[1].direction, Direction.RIGHT)


class TestRotationSimulation(unittest.TestCase):
    """Test dial rotation simulation."""

    def test_right_rotation_basic(self):
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 30), False)
        self.assertEqual(result.final_position, 80)
        self.assertEqual(result.zero_crossings, 0)

    def test_right_rotation_with_wrap(self):
        result = simulate_rotation(90, Rotation(Direction.RIGHT, 20), False)
        self.assertEqual(result.final_position, 10)
        self.assertEqual(result.zero_crossings, 0)

    def test_left_rotation_basic(self):
        result = simulate_rotation(50, Rotation(Direction.LEFT, 30), False)
        self.assertEqual(result.final_position, 20)
        self.assertEqual(result.zero_crossings, 0)

    def test_left_rotation_with_wrap(self):
        result = simulate_rotation(10, Rotation(Direction.LEFT, 20), False)
        self.assertEqual(result.final_position, 90)
        self.assertEqual(result.zero_crossings, 0)

    def test_zero_distance(self):
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 0), True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 0)

    def test_count_during_right_multiple_wraps(self):
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 1000), True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 10)

    def test_count_during_left_one_wrap(self):
        result = simulate_rotation(50, Rotation(Direction.LEFT, 68), True)
        self.assertEqual(result.final_position, 82)
        self.assertEqual(result.zero_crossings, 1)

    def test_count_during_vs_after_ends_at_zero(self):
        # When ending at 0, both modes should count it
        result_during = simulate_rotation(48, Rotation(Direction.RIGHT, 52), True)
        result_after = simulate_rotation(48, Rotation(Direction.RIGHT, 52), False)
        self.assertEqual(result_during.final_position, 0)
        self.assertEqual(result_after.final_position, 0)
        self.assertEqual(result_during.zero_crossings, 1)
        self.assertEqual(result_after.zero_crossings, 1)

    def test_count_during_vs_after_not_at_zero(self):
        # When not ending at 0, only during mode counts crossings
        result_during = simulate_rotation(50, Rotation(Direction.RIGHT, 1000), True)
        result_after = simulate_rotation(50, Rotation(Direction.RIGHT, 1000), False)
        self.assertEqual(result_during.zero_crossings, 10)
        self.assertEqual(result_after.zero_crossings, 0)

    def test_large_distance_performance(self):
        # This should complete instantly (O(1)) not iterate through 1M clicks
        import time

        start = time.time()
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 1000000), True)
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.01)  # Should be nearly instant
        self.assertEqual(result.zero_crossings, 10000)


class TestPasswordCalculation(unittest.TestCase):
    """Test complete password calculation."""

    EXAMPLE_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    def test_part1_example(self):
        """Test Part 1 with example input - should produce password 3."""
        result = solve_part1(self.EXAMPLE_INPUT)
        self.assertEqual(result, 3)

    def test_part2_example(self):
        """Test Part 2 with example input - should produce password 6."""
        result = solve_part2(self.EXAMPLE_INPUT)
        self.assertEqual(result, 6)

    def test_step_by_step_standard(self):
        """Validate step-by-step execution for Standard method."""
        rotations = parse_rotations(self.EXAMPLE_INPUT)
        position = 50
        count = 0

        # L68: 50 -> 82, no zero
        result = simulate_rotation(position, rotations[0], False)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 82)
        self.assertEqual(count, 0)

        # L30: 82 -> 52, no zero
        result = simulate_rotation(position, rotations[1], False)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 52)
        self.assertEqual(count, 0)

        # R48: 52 -> 0, YES zero!
        result = simulate_rotation(position, rotations[2], False)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 0)
        self.assertEqual(count, 1)

    def test_step_by_step_click_method(self):
        """Validate step-by-step execution for Click Method."""
        rotations = parse_rotations(self.EXAMPLE_INPUT)
        position = 50
        count = 0

        # L68: 50 -> 82, crosses 0 once (wraps backward)
        result = simulate_rotation(position, rotations[0], True)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 82)
        self.assertEqual(count, 1)

        # L30: 82 -> 52, no crossings
        result = simulate_rotation(position, rotations[1], True)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 52)
        self.assertEqual(count, 1)

        # R48: 52 -> 0, crosses 0 once (wraps forward and ends at 0)
        result = simulate_rotation(position, rotations[2], True)
        position = result.final_position
        count += result.zero_crossings
        self.assertEqual(position, 0)
        self.assertEqual(count, 2)

    def test_empty_rotations(self):
        """Test with no rotations."""
        result = calculate_password([], PasswordMethod.STANDARD)
        self.assertEqual(result, 0)

    def test_single_rotation_ends_at_zero(self):
        """Test single rotation ending at 0."""
        rotations = [Rotation(Direction.LEFT, 50)]
        result = calculate_password(rotations, PasswordMethod.STANDARD)
        self.assertEqual(result, 1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_rotation_ending_at_zero(self):
        """Test rotation that ends exactly at 0."""
        result = simulate_rotation(48, Rotation(Direction.RIGHT, 52), False)
        self.assertEqual(result.final_position, 0)
        self.assertEqual(result.zero_crossings, 1)

    def test_rotation_from_zero_left(self):
        """Test left rotation from position 0."""
        result = simulate_rotation(0, Rotation(Direction.LEFT, 1), False)
        self.assertEqual(result.final_position, 99)
        self.assertEqual(result.zero_crossings, 0)

    def test_rotation_from_zero_right(self):
        """Test right rotation from position 0."""
        result = simulate_rotation(0, Rotation(Direction.RIGHT, 1), False)
        self.assertEqual(result.final_position, 1)
        self.assertEqual(result.zero_crossings, 0)

    def test_rotation_to_99_wraps_to_zero(self):
        """Test that right rotation from 99 wraps to 0."""
        result = simulate_rotation(99, Rotation(Direction.RIGHT, 1), True)
        self.assertEqual(result.final_position, 0)
        self.assertEqual(result.zero_crossings, 1)

    def test_large_rotation_multiple_wraps(self):
        """Test large rotation with multiple wraps."""
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 1000), True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 10)

    def test_exact_100_rotation(self):
        """Test rotation of exactly 100 (one complete circle)."""
        result = simulate_rotation(50, Rotation(Direction.RIGHT, 100), True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 1)

    def test_parse_negative_distance_error(self):
        """Test that negative distances raise ValueError."""
        with self.assertRaises(ValueError):
            parse_rotation("R-10")

    def test_empty_input(self):
        """Test parsing empty input."""
        rotations = parse_rotations("")
        self.assertEqual(len(rotations), 0)

    def test_file_not_found(self):
        """Test that missing file raises FileNotFoundError."""
        from agent import read_input_file

        with self.assertRaises(FileNotFoundError):
            read_input_file("nonexistent_file.txt")


def performance_test():
    """Validate performance with large inputs."""
    import time

    # Test 1: Many rotations
    rotations = [Rotation(Direction.RIGHT, 50) for _ in range(1000)]
    start = time.time()
    result = calculate_password(rotations, PasswordMethod.CLICK_METHOD)
    elapsed = time.time() - start
    print(f"\nPerformance Test (1000 rotations):")
    print(f"  Part 2 password: {result}")
    print(f"  Time: {elapsed:.4f}s")
    assert elapsed < 1.0, f"Performance test failed: {elapsed}s > 1.0s"

    # Test 2: Very large distance
    rotations = [Rotation(Direction.RIGHT, 1000000)]
    start = time.time()
    result = simulate_rotation(50, rotations[0], True)
    elapsed = time.time() - start
    print(f"\nLarge Distance Test (1M clicks):")
    print(f"  Zero crossings: {result.zero_crossings}")
    print(f"  Time: {elapsed:.6f}s")
    assert elapsed < 0.01, f"Large distance test failed: {elapsed}s > 0.01s"

    print("\n✓ Performance validation passed")


if __name__ == "__main__":
    # Run performance tests first
    performance_test()
    print("\n" + "=" * 70)
    print("Running unit tests...")
    print("=" * 70)

    # Then run unit tests
    unittest.main()
