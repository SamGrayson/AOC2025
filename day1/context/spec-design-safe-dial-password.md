---
title: Safe Dial Password Calculator - Day 1 Advent of Code 2025
version: 1.0
date_created: 2025-12-01
last_updated: 2025-12-01
owner: Sam Grayson
tags: [design, aoc2025, day1, algorithm]
---

# Introduction

This specification defines the requirements for a safe dial password calculator that processes rotation instructions to determine the password for a secure entrance. The solution must support two different password calculation methods: counting zero positions after rotations (Part 1) and counting all zero crossings including during rotations (Part 2).

## 1. Purpose & Scope

**Purpose**: Design a solution to calculate the password for a circular dial safe by tracking when the dial points at zero during a sequence of left/right rotations.

**Scope**: This specification covers:

- Parsing rotation instructions from input text
- Simulating dial rotations on a 0-99 circular number line
- Counting zero positions using two different methods
- Supporting both parts of the challenge with shared, reusable code

**Audience**: AI code generation systems and developers implementing the solution.

**Assumptions**:

- Input is well-formed with one rotation instruction per line
- All rotation instructions follow the format: `[L|R][distance]` where distance is a positive integer
- The dial has exactly 100 positions numbered 0-99

## 2. Definitions

- **Dial**: A circular number line with positions 0 through 99
- **Rotation**: A movement instruction specifying direction (L/R) and distance (number of clicks)
- **Click**: A single movement of one position on the dial
- **Zero Crossing**: Any instance where the dial points at position 0
- **Password Method Standard**: Count zero positions only after completing each rotation (Part 1)
- **Password Method 0x434C49434B**: Count all zero crossings including during rotations (Part 2)
- **L**: Left rotation (toward lower numbers, wrapping from 0 to 99)
- **R**: Right rotation (toward higher numbers, wrapping from 99 to 0)

## 3. Requirements, Constraints & Guidelines

### Functional Requirements

- **REQ-001**: The system shall parse rotation instructions from text input, one instruction per line
- **REQ-002**: Each rotation instruction shall be parsed into a direction (L or R) and a distance (positive integer)
- **REQ-003**: The dial shall start at position 50
- **REQ-004**: The dial shall support 100 positions numbered 0 through 99
- **REQ-005**: Left rotations shall decrease the dial position (wrapping from 0 to 99)
- **REQ-006**: Right rotations shall increase the dial position (wrapping from 99 to 0)
- **REQ-007**: The system shall support Standard password method (count zeros after rotations only)
- **REQ-008**: The system shall support 0x434C49434B password method (count all zero crossings)
- **REQ-009**: The system shall return the total count of zero crossings based on the selected method

### Constraints

- **CON-001**: The dial has exactly 100 positions (0-99)
- **CON-002**: The dial always starts at position 50
- **CON-003**: Position wrapping must be implemented using modulo arithmetic for correctness
- **CON-004**: Rotation distances can be arbitrarily large (e.g., R1000)
- **CON-005**: Input format is fixed: direction letter followed immediately by distance number

### Guidelines

- **GUD-001**: Use a single rotation simulation function for both password methods
- **GUD-002**: Extract rotation parsing logic into a separate, reusable function
- **GUD-003**: Use descriptive names for password methods (avoid magic strings)
- **GUD-004**: Handle edge cases explicitly (zero distance rotations, wrapping boundaries)
- **GUD-005**: Structure code to minimize duplication between Part 1 and Part 2 solutions

### Code Quality Requirements

- **CQ-001**: All code must follow KISS principle - favor simple, readable solutions over clever optimizations
- **CQ-002**: All code must follow DRY principle - rotation logic should be implemented once and reused
- **CQ-003**: All code must follow YAGNI principle - implement only the two required password methods
- **CQ-004**: All code must follow SOLID principles:
  - Single Responsibility: Separate parsing, rotation simulation, and counting logic
  - Open/Closed: Design to support both password methods without modifying core rotation logic
- **CQ-005**: Time complexity should be O(n\*m) where n=number of rotations, m=average distance per rotation
- **CQ-006**: Space complexity should be O(1) - no need to store rotation history
- **CQ-007**: Variable and function names must clearly indicate purpose (e.g., `count_zero_crossings`, `parse_rotation`)

### Design Patterns

- **PAT-001**: Use Strategy pattern or parameterization to switch between password methods
- **PAT-002**: Use a rotation result object/tuple to return both final position and zero count
- **PAT-003**: Implement rotation simulation as a pure function (no side effects)

## 4. Interfaces & Data Contracts

### Input Format

```
L68
L30
R48
L5
...
```

Each line contains:

- Direction: Single character 'L' or 'R'
- Distance: Positive integer (no leading zeros, arbitrary length)

### Rotation Instruction Structure

```python
class Rotation:
    direction: str  # 'L' or 'R'
    distance: int   # positive integer
```

### Password Method Enumeration

```python
class PasswordMethod:
    STANDARD = "standard"              # Count zeros after rotations only
    CLICK_METHOD = "0x434C49434B"      # Count all zero crossings
```

### Core Function Signatures

```python
def parse_rotation(line: str) -> Rotation:
    """Parse a single rotation instruction from text."""
    pass

def simulate_rotation(
    start_position: int,
    direction: str,
    distance: int,
    count_during: bool
) -> tuple[int, int]:
    """
    Simulate a dial rotation.

    Args:
        start_position: Current dial position (0-99)
        direction: 'L' for left, 'R' for right
        distance: Number of clicks to rotate
        count_during: Whether to count zero crossings during rotation

    Returns:
        Tuple of (final_position, zero_count)
    """
    pass

def calculate_password(
    rotations: list[Rotation],
    method: PasswordMethod
) -> int:
    """
    Calculate password by processing all rotations.

    Args:
        rotations: List of rotation instructions
        method: Password calculation method to use

    Returns:
        Total count of zero crossings
    """
    pass
```

## 5. Acceptance Criteria

### Part 1 - Standard Password Method

- **AC-001**: Given the example input, When using Standard method, Then the password shall be 3
- **AC-002**: Given the dial starts at 50, When rotated L68, Then it shall point at 82
- **AC-003**: Given the dial is at 82, When rotated L30, Then it shall point at 52
- **AC-004**: Given the dial is at 52, When rotated R48, Then it shall point at 0 and count shall increment
- **AC-005**: Given the dial is at 0, When rotated L5, Then it shall point at 95
- **AC-006**: Given the dial is at 95, When rotated R60, Then it shall point at 55
- **AC-007**: Given the dial is at 55, When rotated L55, Then it shall point at 0 and count shall increment
- **AC-008**: Given the dial is at 0, When rotated L1, Then it shall point at 99
- **AC-009**: Given the dial is at 99, When rotated L99, Then it shall point at 0 and count shall increment
- **AC-010**: Given the dial is at 0, When rotated R14, Then it shall point at 14
- **AC-011**: Given the dial is at 14, When rotated L82, Then it shall point at 32

### Part 2 - Click Method 0x434C49434B

- **AC-020**: Given the example input, When using Click method, Then the password shall be 6
- **AC-021**: Given the dial is at 50, When rotated L68, Then zero shall be crossed once during rotation
- **AC-022**: Given the dial is at 95, When rotated R60, Then zero shall be crossed once during rotation
- **AC-023**: Given the dial is at 14, When rotated L82, Then zero shall be crossed once during rotation
- **AC-024**: Given the dial is at 50, When rotated R1000, Then zero shall be crossed 10 times
- **AC-025**: Given any rotation ending at 0, When using Click method, Then it shall count both during-rotation crossings AND the final position

### Edge Cases

- **AC-030**: Given the dial is at 0, When rotated L0 or R0, Then position shall remain 0 and count shall not increment
- **AC-031**: Given the dial is at 5, When rotated L10, Then it shall point at 95
- **AC-032**: Given the dial is at 95, When rotated R5, Then it shall point at 0
- **AC-033**: Given the dial is at 99, When rotated R1, Then it shall point at 0
- **AC-034**: Given the dial is at 0, When rotated L1, Then it shall point at 99
- **AC-035**: Given a large rotation distance, When the rotation wraps multiple times, Then all zero crossings shall be counted accurately

## 6. Test Automation Strategy

### Test Levels

- **Unit Tests**: Test individual functions (parse_rotation, simulate_rotation)
- **Integration Tests**: Test complete password calculation with example inputs
- **Edge Case Tests**: Verify boundary conditions and wrapping behavior

### Test Framework

- Use Python's built-in `unittest` or `pytest` framework
- Organize tests in a separate `test_day1.py` file
- Use parameterized tests for rotation examples

### Test Data Management

- Store the example input as a test fixture
- Create minimal test cases for boundary conditions
- Generate test cases for large rotation values programmatically

### Coverage Requirements

- Minimum 90% code coverage for core logic
- 100% coverage of rotation simulation function
- All acceptance criteria must have corresponding automated tests

### Test Categories

1. **Parsing Tests**: Validate rotation instruction parsing
2. **Rotation Tests**: Verify dial movement and wrapping
3. **Standard Method Tests**: Validate Part 1 password calculation
4. **Click Method Tests**: Validate Part 2 password calculation
5. **Edge Case Tests**: Boundary values, zero distances, large distances

## 7. Rationale & Context

### Design Decisions

**Circular Number Line Implementation**: The dial wraps around using modulo 100 arithmetic. This ensures mathematical correctness for any rotation distance without requiring separate wrap-around logic.

**Two Password Methods**: Part 2 extends Part 1 by requiring more granular tracking. The design uses a boolean flag (`count_during`) to enable/disable during-rotation counting, allowing code reuse.

**Separation of Concerns**: Parsing, simulation, and counting are separate responsibilities to enable independent testing and modification.

**Strategy Pattern**: Rather than duplicating rotation logic, a parameter controls counting behavior. This follows the Open/Closed principle.

### Algorithm Complexity

**Time Complexity**: For n rotations with average distance m, the complexity is O(n\*m) when counting during rotations. For large distances (like R1000), we could optimize by calculating crossings mathematically rather than iterating, reducing to O(n).

**Space Complexity**: O(1) - only tracking current position and count.

**Optimization Opportunity**: For Part 2, zero crossings during a rotation can be calculated mathematically:

- For right rotation from position p with distance d: `crossings = (p + d) // 100`
- For left rotation from position p with distance d: `crossings = (d - p + 99) // 100`

This would reduce time complexity to O(n) for both parts.

### Example Walkthrough Logic

The example demonstrates key edge cases:

1. **Wrapping left**: L68 from 50 crosses 0 once (50→49→...→1→0→99→...→82)
2. **Wrapping right**: R60 from 95 crosses 0 once (95→96→...→99→0→...→55)
3. **Direct landing on 0**: R48 from 52, L55 from 55, L99 from 99 all end at 0
4. **Multiple wraps**: The note about R1000 from 50 demonstrates 10 full circles

## 8. Dependencies & External Integrations

### Standard Library Dependencies

- **STD-001**: Python standard library `re` module - For robust rotation instruction parsing (optional, string operations may suffice)
- **STD-002**: Python standard library `typing` module - For type hints and improved code clarity

### Runtime Dependencies

- **PLT-001**: Python 3.8+ - Required for modern type hinting syntax and walrus operator (if used)

### Data Dependencies

- **DAT-001**: Input file (`input.txt`) - Contains newline-delimited rotation instructions in format `[L|R][distance]`

**Note**: This solution has minimal dependencies and uses only Python standard library features. No external packages or services are required.

## 9. Validation Criteria

### Correctness Validation

- **VAL-001**: Solution must produce password value of 3 for the example input using Standard method
- **VAL-002**: Solution must produce password value of 6 for the example input using Click method
- **VAL-003**: All 11 rotation steps in the example must produce correct intermediate positions
- **VAL-004**: Edge case rotations (L10 from 5, R5 from 95) must produce correct positions

### Performance Validation

- **VAL-005**: Solution must process 1000 rotations in under 1 second for Standard method
- **VAL-006**: Solution must handle rotation distances up to 1,000,000 efficiently
- **VAL-007**: Memory usage must remain constant regardless of number of rotations

### Code Quality Validation

- **VAL-008**: Code must pass type checking with mypy or similar tool
- **VAL-009**: Code must have no linting errors with flake8 or ruff
- **VAL-010**: All functions must have docstrings describing parameters and return values

## 10. Related Specifications / Further Reading

### Advent of Code 2025

- [Day 1 Challenge](https://adventofcode.com/2025/day/1)
- [Advent of Code About Page](https://adventofcode.com/about)

### Algorithm References

- [Modulo Arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic) - For circular number line wrapping
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy) - For multiple password calculation methods

### Python Best Practices

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python SOLID Principles](https://realpython.com/solid-principles-python/)
