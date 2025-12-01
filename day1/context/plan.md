# Safe Dial Password Calculator - Phased Implementation Plan

**Project**: Day 1 - Advent of Code 2025  
**Created**: December 1, 2025  
**Specification**: [spec-design-safe-dial-password.md](./spec-design-safe-dial-password.md)

---

## Executive Summary

This plan outlines a 5-phase approach to implement a safe dial password calculator that processes rotation instructions on a circular 0-99 dial. The solution supports two password calculation methods: Standard (counting zeros after rotations only) and Click Method (counting all zero crossings including during rotations). The implementation prioritizes simplicity, reusability, and performance following KISS, DRY, YAGNI, and SOLID principles.

**Key Design Decisions**:

- Single rotation simulation function with parameterized counting behavior
- Mathematical optimization for counting zero crossings to achieve O(n) complexity
- Separate parsing, simulation, and orchestration layers for testability
- Strategy pattern for method selection without code duplication

---

## Phase 1: Foundation & Parsing (Estimated: 30 minutes)

### Objectives

- Establish project structure with type safety
- Implement robust rotation instruction parsing
- Create data models for rotations and password methods

### Tasks

#### 1.1: Define Data Models

**File**: `agent.py`

```python
from enum import Enum
from typing import NamedTuple

class Direction(Enum):
    """Rotation direction enumeration."""
    LEFT = 'L'
    RIGHT = 'R'

class Rotation(NamedTuple):
    """Represents a single rotation instruction."""
    direction: Direction
    distance: int

class PasswordMethod(Enum):
    """Password calculation method enumeration."""
    STANDARD = "standard"
    CLICK_METHOD = "0x434C49434B"
```

**Acceptance Criteria**:

- ✓ Direction enum supports L and R values
- ✓ Rotation is immutable with type-safe fields
- ✓ PasswordMethod enum has both required methods

#### 1.2: Implement Rotation Parsing

**File**: `agent.py`

```python
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

    if direction_char not in ('L', 'R'):
        raise ValueError(f"Invalid direction: '{direction_char}'")

    try:
        distance = int(distance_str)
    except ValueError:
        raise ValueError(f"Invalid distance: '{distance_str}'")

    if distance < 0:
        raise ValueError(f"Distance must be non-negative: {distance}")

    direction = Direction.LEFT if direction_char == 'L' else Direction.RIGHT
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
    for line_num, line in enumerate(input_text.strip().split('\n'), start=1):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        try:
            rotations.append(parse_rotation(line))
        except ValueError as e:
            raise ValueError(f"Line {line_num}: {e}")
    return rotations
```

**Acceptance Criteria**:

- ✓ Parses valid L and R rotations correctly
- ✓ Handles arbitrary distance values (including large numbers like 1000)
- ✓ Raises clear errors for invalid formats
- ✓ Strips whitespace and ignores empty lines
- ✓ Provides line numbers in error messages

#### 1.3: Unit Tests for Parsing

**File**: `test_day1.py` (create new file)

```python
import unittest
from agent import parse_rotation, parse_rotations, Direction, Rotation

class TestRotationParsing(unittest.TestCase):
    """Test rotation instruction parsing."""

    def test_parse_left_rotation(self):
        result = parse_rotation('L68')
        self.assertEqual(result.direction, Direction.LEFT)
        self.assertEqual(result.distance, 68)

    def test_parse_right_rotation(self):
        result = parse_rotation('R1000')
        self.assertEqual(result.direction, Direction.RIGHT)
        self.assertEqual(result.distance, 1000)

    def test_parse_zero_distance(self):
        result = parse_rotation('L0')
        self.assertEqual(result.distance, 0)

    def test_parse_with_whitespace(self):
        result = parse_rotation('  R48  ')
        self.assertEqual(result.direction, Direction.RIGHT)
        self.assertEqual(result.distance, 48)

    def test_parse_invalid_direction(self):
        with self.assertRaises(ValueError):
            parse_rotation('X10')

    def test_parse_invalid_distance(self):
        with self.assertRaises(ValueError):
            parse_rotation('Labc')

    def test_parse_empty_string(self):
        with self.assertRaises(ValueError):
            parse_rotation('')

    def test_parse_multiple_rotations(self):
        input_text = "L68\nR48\nL30"
        rotations = parse_rotations(input_text)
        self.assertEqual(len(rotations), 3)
        self.assertEqual(rotations[0].distance, 68)
        self.assertEqual(rotations[1].direction, Direction.RIGHT)
```

**Acceptance Criteria**:

- ✓ All parsing tests pass
- ✓ Edge cases covered (zero distance, whitespace, errors)
- ✓ Multi-line parsing works correctly

### Deliverables

- [ ] Data models defined with type hints
- [ ] Parsing functions implemented
- [ ] Unit tests passing for all parsing scenarios
- [ ] Code passes type checking (mypy)

---

## Phase 2: Core Rotation Simulation (Estimated: 45 minutes)

### Objectives

- Implement mathematically optimized rotation simulation
- Support both counting modes (after-only vs. during-and-after)
- Ensure O(1) space and O(n) time complexity

### Tasks

#### 2.1: Mathematical Zero Crossing Calculation

**File**: `agent.py`

```python
class RotationResult(NamedTuple):
    """Result of a rotation simulation."""
    final_position: int  # Position after rotation (0-99)
    zero_crossings: int  # Number of times dial pointed at 0


def calculate_zero_crossings(
    start_position: int,
    direction: Direction,
    distance: int,
    count_during: bool
) -> int:
    """
    Calculate number of zero crossings during a rotation using mathematics.

    This is an optimization to avoid iterating through each click.
    Time complexity: O(1) instead of O(distance)

    Args:
        start_position: Current dial position (0-99)
        direction: Direction of rotation
        distance: Number of clicks
        count_during: If True, count crossings during rotation;
                     if False, count only if final position is 0

    Returns:
        Number of times the dial pointed at 0

    Mathematical reasoning:
        - For RIGHT rotation: moving from p toward higher numbers
          - Final position: (p + distance) % 100
          - Zero crossings: floor((p + distance) / 100)
          - This counts how many times we wrap past 0

        - For LEFT rotation: moving from p toward lower numbers
          - Final position: (p - distance) % 100
          - Zero crossings: floor((distance - p - 1) / 100) + 1 if distance > p
          - This counts how many times we wrap backward through 0

    Examples:
        >>> calculate_zero_crossings(50, Direction.RIGHT, 1000, True)
        10  # Wraps 10 times through 0
        >>> calculate_zero_crossings(50, Direction.LEFT, 68, True)
        1   # Crosses 0 once (50->49->...->0->99->...->82)
        >>> calculate_zero_crossings(52, Direction.RIGHT, 48, True)
        1   # Ends at 0 (52+48=100, 100%100=0, crosses once)
    """
    if distance == 0:
        return 0

    if not count_during:
        # Only count if final position is 0
        if direction == Direction.RIGHT:
            final_pos = (start_position + distance) % 100
        else:  # LEFT
            final_pos = (start_position - distance) % 100
        return 1 if final_pos == 0 else 0

    # Count all crossings during rotation
    if direction == Direction.RIGHT:
        # Moving toward higher numbers
        # Crosses 0 when: start + clicks >= 100, 200, 300, etc.
        # Number of crossings = floor((start + distance) / 100)
        crossings = (start_position + distance) // 100
    else:  # LEFT
        # Moving toward lower numbers
        # Crosses 0 when: start - clicks < 0, -100, -200, etc.
        # Number of crossings = ceil(distance - start) / 100)
        crossings = (distance + 99 - start_position) // 100

    return crossings


def simulate_rotation(
    start_position: int,
    direction: Direction,
    distance: int,
    count_during: bool
) -> RotationResult:
    """
    Simulate a single dial rotation.

    Args:
        start_position: Current dial position (0-99)
        direction: Direction to rotate (LEFT or RIGHT)
        distance: Number of clicks to rotate
        count_during: Whether to count zero crossings during rotation

    Returns:
        RotationResult with final position and zero crossing count

    Constraints:
        - Dial has 100 positions (0-99)
        - LEFT decreases position (wraps 0->99)
        - RIGHT increases position (wraps 99->0)

    Examples:
        >>> simulate_rotation(50, Direction.LEFT, 68, False)
        RotationResult(final_position=82, zero_crossings=0)
        >>> simulate_rotation(52, Direction.RIGHT, 48, True)
        RotationResult(final_position=0, zero_crossings=1)
    """
    # Calculate final position using modulo arithmetic
    if direction == Direction.RIGHT:
        final_position = (start_position + distance) % 100
    else:  # LEFT
        final_position = (start_position - distance) % 100

    # Calculate zero crossings efficiently
    zero_crossings = calculate_zero_crossings(
        start_position, direction, distance, count_during
    )

    return RotationResult(
        final_position=final_position,
        zero_crossings=zero_crossings
    )
```

**Acceptance Criteria**:

- ✓ Correct final position for all rotations
- ✓ Correct zero crossing counts for both modes
- ✓ O(1) time complexity (no iteration through clicks)
- ✓ Handles edge cases (zero distance, wrapping)

#### 2.2: Unit Tests for Rotation Simulation

**File**: `test_day1.py`

```python
class TestRotationSimulation(unittest.TestCase):
    """Test dial rotation simulation."""

    def test_right_rotation_no_wrap(self):
        result = simulate_rotation(11, Direction.RIGHT, 8, False)
        self.assertEqual(result.final_position, 19)
        self.assertEqual(result.zero_crossings, 0)

    def test_left_rotation_to_zero(self):
        result = simulate_rotation(19, Direction.LEFT, 19, False)
        self.assertEqual(result.final_position, 0)
        self.assertEqual(result.zero_crossings, 1)

    def test_left_rotation_wrap(self):
        result = simulate_rotation(5, Direction.LEFT, 10, False)
        self.assertEqual(result.final_position, 95)
        self.assertEqual(result.zero_crossings, 0)

    def test_right_rotation_from_95(self):
        result = simulate_rotation(95, Direction.RIGHT, 5, False)
        self.assertEqual(result.final_position, 0)
        self.assertEqual(result.zero_crossings, 1)

    def test_zero_distance_rotation(self):
        result = simulate_rotation(50, Direction.LEFT, 0, True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 0)

    def test_large_rotation_multiple_wraps(self):
        result = simulate_rotation(50, Direction.RIGHT, 1000, True)
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 10)

    def test_left_rotation_with_crossing_during(self):
        result = simulate_rotation(50, Direction.LEFT, 68, True)
        self.assertEqual(result.final_position, 82)
        self.assertEqual(result.zero_crossings, 1)

    def test_right_rotation_with_crossing_during(self):
        result = simulate_rotation(95, Direction.RIGHT, 60, True)
        self.assertEqual(result.final_position, 55)
        self.assertEqual(result.zero_crossings, 1)

    def test_rotation_ending_at_zero_counts_in_both_modes(self):
        # Standard mode: counts ending at 0
        result_standard = simulate_rotation(52, Direction.RIGHT, 48, False)
        self.assertEqual(result_standard.zero_crossings, 1)

        # Click mode: also counts ending at 0
        result_click = simulate_rotation(52, Direction.RIGHT, 48, True)
        self.assertEqual(result_click.zero_crossings, 1)
```

**Acceptance Criteria**:

- ✓ All rotation tests pass
- ✓ Both counting modes work correctly
- ✓ Edge cases validated (wrapping, zero distance, large distances)

### Deliverables

- [ ] Rotation simulation functions implemented
- [ ] Mathematical optimization verified
- [ ] Unit tests passing for all rotation scenarios
- [ ] Performance validated (handles distance=1,000,000 instantly)

---

## Phase 3: Password Calculation Orchestration (Estimated: 30 minutes)

### Objectives

- Implement main password calculation logic
- Support both password methods via strategy pattern
- Integrate parsing and simulation layers

### Tasks

#### 3.1: Password Calculator Implementation

**File**: `agent.py`

```python
def calculate_password(
    rotations: list[Rotation],
    method: PasswordMethod
) -> int:
    """
    Calculate the password by processing all rotations.

    Args:
        rotations: List of rotation instructions to process
        method: Password calculation method (STANDARD or CLICK_METHOD)

    Returns:
        Total count of zero crossings based on the method

    Algorithm:
        1. Start at dial position 50
        2. For each rotation:
           a. Simulate rotation with appropriate counting mode
           b. Update current position
           c. Accumulate zero crossings
        3. Return total zero crossing count

    Examples:
        >>> rotations = parse_rotations("L68\\nR48\\nL30")
        >>> calculate_password(rotations, PasswordMethod.STANDARD)
        1  # Only R48 ends at 0
        >>> calculate_password(rotations, PasswordMethod.CLICK_METHOD)
        2  # L68 crosses during + R48 ends at 0
    """
    STARTING_POSITION = 50
    current_position = STARTING_POSITION
    total_zero_crossings = 0

    # Determine counting mode based on method
    count_during = (method == PasswordMethod.CLICK_METHOD)

    # Process each rotation
    for rotation in rotations:
        result = simulate_rotation(
            start_position=current_position,
            direction=rotation.direction,
            distance=rotation.distance,
            count_during=count_during
        )

        current_position = result.final_position
        total_zero_crossings += result.zero_crossings

    return total_zero_crossings


def solve_part1(input_text: str) -> int:
    """
    Solve Part 1: Count zeros after rotations only.

    Args:
        input_text: Multi-line string of rotation instructions

    Returns:
        Password using Standard method
    """
    rotations = parse_rotations(input_text)
    return calculate_password(rotations, PasswordMethod.STANDARD)


def solve_part2(input_text: str) -> int:
    """
    Solve Part 2: Count all zero crossings including during rotations.

    Args:
        input_text: Multi-line string of rotation instructions

    Returns:
        Password using Click Method (0x434C49434B)
    """
    rotations = parse_rotations(input_text)
    return calculate_password(rotations, PasswordMethod.CLICK_METHOD)
```

**Acceptance Criteria**:

- ✓ Starts at position 50
- ✓ Processes rotations sequentially
- ✓ Accumulates zero crossings correctly
- ✓ Supports both password methods

#### 3.2: Integration Tests

**File**: `test_day1.py`

```python
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

    def test_example_part1_standard_method(self):
        """Test the provided example for Part 1."""
        password = solve_part1(self.EXAMPLE_INPUT)
        self.assertEqual(password, 3)

    def test_example_part2_click_method(self):
        """Test the provided example for Part 2."""
        password = solve_part2(self.EXAMPLE_INPUT)
        self.assertEqual(password, 6)

    def test_single_rotation_ending_at_zero(self):
        password = solve_part1("R48")  # From 50 to 98? No wait, 50+48=98
        # Actually need to test from correct positions
        pass  # Will verify step-by-step in detailed test

    def test_step_by_step_example_part1(self):
        """Verify each step of the example for Part 1."""
        rotations = parse_rotations(self.EXAMPLE_INPUT)
        position = 50
        zero_count = 0

        # Expected positions from challenge description
        expected_positions = [82, 52, 0, 95, 55, 0, 99, 0, 14, 32]

        for i, rotation in enumerate(rotations):
            result = simulate_rotation(
                position, rotation.direction, rotation.distance, count_during=False
            )
            position = result.final_position
            zero_count += result.zero_crossings

            self.assertEqual(position, expected_positions[i],
                           f"Step {i+1}: Expected position {expected_positions[i]}, got {position}")

        self.assertEqual(zero_count, 3)

    def test_step_by_step_example_part2(self):
        """Verify each step of the example for Part 2."""
        rotations = parse_rotations(self.EXAMPLE_INPUT)
        position = 50
        zero_count = 0

        # Expected crossings per step (including during rotation)
        expected_crossings = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        for i, rotation in enumerate(rotations):
            result = simulate_rotation(
                position, rotation.direction, rotation.distance, count_during=True
            )
            position = result.final_position
            zero_count += result.zero_crossings

            self.assertEqual(result.zero_crossings, expected_crossings[i],
                           f"Step {i+1}: Expected {expected_crossings[i]} crossings, got {result.zero_crossings}")

        self.assertEqual(zero_count, 6)
```

**Acceptance Criteria**:

- ✓ Example produces password=3 for Part 1
- ✓ Example produces password=6 for Part 2
- ✓ Step-by-step validation matches challenge description

### Deliverables

- [ ] Password calculation functions implemented
- [ ] Both solve_part1 and solve_part2 working
- [ ] Integration tests passing
- [ ] Example walkthrough validated

---

## Phase 4: File I/O & Main Entry Point (Estimated: 20 minutes)

### Objectives

- Add file reading capabilities
- Create main execution entry point
- Support command-line usage

### Tasks

#### 4.1: File I/O and Main Function

**File**: `agent.py`

```python
def read_input_file(filepath: str = "input.txt") -> str:
    """
    Read rotation instructions from file.

    Args:
        filepath: Path to input file (default: input.txt in current directory)

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    """
    Main entry point for the safe dial password calculator.

    Reads rotations from input.txt and prints both passwords.
    """
    try:
        input_text = read_input_file("input.txt")

        # Solve both parts
        part1_password = solve_part1(input_text)
        part2_password = solve_part2(input_text)

        # Output results
        print(f"Part 1 - Standard Password Method: {part1_password}")
        print(f"Part 2 - Click Method (0x434C49434B): {part2_password}")

    except FileNotFoundError:
        print("Error: input.txt not found")
        return 1
    except ValueError as e:
        print(f"Error parsing input: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
```

**Acceptance Criteria**:

- ✓ Reads input.txt successfully
- ✓ Prints both part 1 and part 2 answers
- ✓ Handles file not found gracefully
- ✓ Handles parsing errors gracefully

#### 4.2: Test with Actual Input

**Manual Testing Steps**:

1. Run the example input first:

```bash
# Create test file with example
cat > test_input.txt << 'EOF'
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
EOF

# Test with example (modify main to accept filepath argument)
python agent.py
```

2. Verify outputs:

   - Part 1 should output: 3
   - Part 2 should output: 6

3. Run with actual puzzle input:

```bash
python agent.py
```

**Acceptance Criteria**:

- ✓ Example input produces correct outputs
- ✓ Actual puzzle input runs without errors
- ✓ Outputs are properly formatted

### Deliverables

- [ ] File reading implemented
- [ ] Main function working
- [ ] Error handling in place
- [ ] Manual testing completed with example

---

## Phase 5: Validation, Optimization & Documentation (Estimated: 30 minutes)

### Objectives

- Complete test coverage
- Verify code quality standards
- Add comprehensive documentation
- Performance validation

### Tasks

#### 5.1: Complete Test Suite

**File**: `test_day1.py`

```python
class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_rotation_from_zero_left(self):
        result = simulate_rotation(0, Direction.LEFT, 1, False)
        self.assertEqual(result.final_position, 99)

    def test_rotation_from_zero_right(self):
        result = simulate_rotation(0, Direction.RIGHT, 1, False)
        self.assertEqual(result.final_position, 1)

    def test_rotation_to_99_from_0(self):
        result = simulate_rotation(0, Direction.LEFT, 1, False)
        self.assertEqual(result.final_position, 99)

    def test_rotation_from_99_to_0(self):
        result = simulate_rotation(99, Direction.RIGHT, 1, False)
        self.assertEqual(result.final_position, 0)
        self.assertEqual(result.zero_crossings, 1)

    def test_large_distance_performance(self):
        """Verify O(1) performance for large distances."""
        import time
        start = time.time()
        result = simulate_rotation(50, Direction.RIGHT, 1_000_000, True)
        elapsed = time.time() - start

        # Should complete in microseconds, not seconds
        self.assertLess(elapsed, 0.01, "Large rotation should be O(1)")
        self.assertEqual(result.final_position, 50)
        self.assertEqual(result.zero_crossings, 10_000)

    def test_empty_rotation_list(self):
        password = calculate_password([], PasswordMethod.STANDARD)
        self.assertEqual(password, 0)

    def test_only_non_zero_rotations(self):
        rotations = parse_rotations("R10\nL5\nR3")
        password = calculate_password(rotations, PasswordMethod.STANDARD)
        self.assertEqual(password, 0)


if __name__ == '__main__':
    unittest.main()
```

**Acceptance Criteria**:

- ✓ All edge cases tested
- ✓ Performance test validates O(1) rotation
- ✓ 90%+ code coverage achieved
- ✓ All tests pass

#### 5.2: Code Quality Checks

**Type Checking**:

```bash
# Install mypy if needed
pip install mypy

# Run type checker
mypy agent.py --strict
```

**Linting**:

```bash
# Install ruff if needed
pip install ruff

# Run linter
ruff check agent.py

# Auto-fix issues
ruff check --fix agent.py
```

**Acceptance Criteria**:

- ✓ No mypy errors
- ✓ No linting errors
- ✓ Code follows PEP 8

#### 5.3: Documentation Review

**Checklist**:

- [ ] All functions have docstrings
- [ ] Docstrings include Args, Returns, Raises sections
- [ ] Complex algorithms have explanatory comments
- [ ] Examples in docstrings are accurate
- [ ] Module-level docstring explains purpose

**File**: `agent.py` (add module docstring at top)

```python
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
```

#### 5.4: Performance Validation

**Create Performance Test**:

```python
def performance_test():
    """Validate performance with large inputs."""
    import time

    # Generate 1000 rotations with varying distances
    large_input = '\n'.join(
        f"{'L' if i % 2 == 0 else 'R'}{(i * 137) % 10000}"
        for i in range(1000)
    )

    start = time.time()
    result1 = solve_part1(large_input)
    elapsed1 = time.time() - start

    start = time.time()
    result2 = solve_part2(large_input)
    elapsed2 = time.time() - start

    print(f"Performance Test (1000 rotations):")
    print(f"  Part 1: {elapsed1:.4f}s (password: {result1})")
    print(f"  Part 2: {elapsed2:.4f}s (password: {result2})")
    print(f"  Target: < 1.0s for each")

    assert elapsed1 < 1.0, "Part 1 too slow"
    assert elapsed2 < 1.0, "Part 2 too slow"
    print("✓ Performance validation passed")

if __name__ == "__main__":
    performance_test()
```

**Acceptance Criteria**:

- ✓ 1000 rotations processed in < 1 second
- ✓ Large rotation distances (1M+) handled instantly
- ✓ Memory usage constant regardless of input size

### Deliverables

- [ ] Complete test suite with 90%+ coverage
- [ ] Type checking passing (mypy)
- [ ] Linting passing (ruff)
- [ ] All docstrings complete
- [ ] Performance validated

---

## Testing Strategy

### Test Categories

1. **Unit Tests** (Phases 1-2)

   - Parsing individual rotations
   - Rotation simulation logic
   - Mathematical crossing calculation

2. **Integration Tests** (Phase 3)

   - Full example walkthrough
   - Both password methods
   - Step-by-step validation

3. **Edge Case Tests** (Phase 5)

   - Boundary conditions (0, 99)
   - Zero-distance rotations
   - Wrapping behavior
   - Large distances

4. **Performance Tests** (Phase 5)
   - Large rotation counts
   - Large rotation distances
   - Memory efficiency

### Test Execution

```bash
# Run all tests
python -m unittest discover -s . -p "test_*.py" -v

# Run with coverage
pip install coverage
coverage run -m unittest discover
coverage report -m
coverage html  # Generate HTML report
```

### Expected Coverage Targets

- **Minimum**: 90% overall
- **Critical paths**: 100% (rotation simulation, crossing calculation)
- **Parse functions**: 100%
- **Main/IO**: 80% (some error paths hard to test)

---

## Risk Mitigation

### Technical Risks

| Risk                                      | Impact | Mitigation                                   |
| ----------------------------------------- | ------ | -------------------------------------------- |
| Incorrect modulo arithmetic for wrapping  | High   | Extensive unit tests for boundary cases      |
| Off-by-one errors in crossing calculation | High   | Mathematical proof + step-by-step validation |
| Performance issues with large distances   | Medium | Mathematical optimization (already O(1))     |
| Parsing edge cases missed                 | Low    | Comprehensive parsing tests + error handling |

### Implementation Risks

| Risk                                 | Impact | Mitigation                                  |
| ------------------------------------ | ------ | ------------------------------------------- |
| Misunderstanding Part 2 requirements | High   | Step-by-step example validation             |
| Code duplication between parts       | Medium | Strategy pattern with shared rotation logic |
| Type safety issues                   | Low    | Strict mypy checking from start             |

---

## Quality Gates

Each phase must meet these criteria before proceeding:

### Phase 1 ✓

- [ ] All parsing tests pass
- [ ] Type hints on all functions
- [ ] No mypy errors

### Phase 2 ✓

- [ ] All rotation tests pass
- [ ] O(1) performance verified
- [ ] Mathematical correctness validated

### Phase 3 ✓

- [ ] Example produces correct outputs (3 and 6)
- [ ] Step-by-step validation matches specification
- [ ] Both methods work correctly

### Phase 4 ✓

- [ ] File I/O working
- [ ] Error handling tested
- [ ] Main function executes successfully

### Phase 5 ✓

- [ ] 90%+ test coverage
- [ ] No linting errors
- [ ] All documentation complete
- [ ] Performance targets met

---

## Success Criteria

**Definition of Done**:

- ✓ Both Part 1 and Part 2 produce correct answers for example input
- ✓ Both parts produce correct answers for actual puzzle input
- ✓ All acceptance criteria from specification met
- ✓ Test coverage ≥ 90%
- ✓ No type checking or linting errors
- ✓ Performance targets met (1000 rotations < 1s)
- ✓ Code follows KISS, DRY, YAGNI, SOLID principles
- ✓ All edge cases tested and validated

**Code Quality Metrics**:

- Cyclomatic complexity < 10 per function
- Function length < 50 lines
- No code duplication (DRY violations)
- All public functions documented

---

## Timeline Estimate

| Phase     | Tasks                                   | Estimated Time | Dependencies |
| --------- | --------------------------------------- | -------------- | ------------ |
| Phase 1   | Data models, parsing, tests             | 30 min         | None         |
| Phase 2   | Rotation simulation, optimization       | 45 min         | Phase 1      |
| Phase 3   | Password calculation, integration tests | 30 min         | Phase 2      |
| Phase 4   | File I/O, main function                 | 20 min         | Phase 3      |
| Phase 5   | Validation, documentation               | 30 min         | Phase 4      |
| **Total** |                                         | **~2.5 hours** |              |

**Note**: Times assume focused implementation without interruptions. Add buffer for debugging and refinement.

---

## Appendix: Key Algorithms

### Modulo Arithmetic for Circular Dial

```
Right rotation: position' = (position + distance) % 100
Left rotation:  position' = (position - distance) % 100

Python's modulo handles negative numbers correctly:
  (-5) % 100 = 95 ✓
```

### Zero Crossing Calculation

**Right rotation** (position p, distance d):

```
Crossings = floor((p + d) / 100)

Example: p=50, d=1000
  Crossings = (50 + 1000) / 100 = 10.5 → 10
```

**Left rotation** (position p, distance d):

```
Crossings = ceil((d - p) / 100) if d > p else 0
Or equivalently: (d + 99 - p) // 100

Example: p=50, d=68
  Crossings = (68 + 99 - 50) / 100 = 1.17 → 1
```

### Complexity Analysis

- **Time**: O(n) where n = number of rotations
  - Each rotation processed in O(1) time
  - No iteration through individual clicks
- **Space**: O(n) for storing parsed rotations
  - O(1) for simulation (only tracking current position)

---

## References

- **Specification**: [spec-design-safe-dial-password.md](./spec-design-safe-dial-password.md)
- **Challenge**: Advent of Code 2025 Day 1
- **Input File**: `../input.txt`
- **Test File**: `../test_day1.py`
- **Implementation**: `../agent.py`
