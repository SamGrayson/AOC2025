# Implementation Plan: Invalid Product ID Detection and Summation

**Specification**: `spec-design-invalid-product-ids.md` v1.0  
**Created**: 2025-12-02  
**Challenge**: Advent of Code 2025 - Day 2

---

## Overview

This plan outlines a phased approach to implementing a solution that identifies and sums invalid product IDs within specified ranges. The solution must handle two distinct validation rules (Part 1: exact double repetition, Part 2: multiple repetitions) while maintaining simplicity, performance, and code reusability.

### Key Design Principles

- **KISS**: Use straightforward pattern detection algorithms
- **DRY**: Share core logic between Part 1 and Part 2 implementations
- **YAGNI**: Focus only on required functionality
- **Performance**: Efficient algorithms for large ranges (millions of IDs)

---

## Phase 1: Input Processing & Infrastructure

**Goal**: Establish robust input parsing and basic infrastructure.

### Tasks

#### 1.1 Input Parser

- **Function**: `parse_input(text: str) -> List[Tuple[int, int]]`
- **Purpose**: Parse comma-separated ranges into list of (start, end) tuples
- **Implementation**:
  - Split input on commas
  - Handle multi-line input (strip whitespace, join lines)
  - Parse each range as "start-end"
  - Convert to integer tuples
  - Validate: start and end are positive integers, start ≤ end
- **Edge Cases**:
  - Trailing/leading whitespace
  - Line breaks within comma-separated list
  - Malformed ranges (handle gracefully or error)

#### 1.2 Test Infrastructure

- **File**: `test_day2.py`
- **Purpose**: Set up pytest test structure
- **Components**:
  - Test fixtures for example input
  - Helper functions for validation
  - Separate test classes for Part 1 and Part 2

#### 1.3 Example Data Extraction

- **Extract from spec**: The example input and expected outputs
- **Part 1 Expected**: `1227775554`
- **Part 2 Expected**: `4174379265`
- **Create test file**: `test_example.txt` with the example ranges

### Acceptance Criteria

- ✅ Parser correctly handles example input
- ✅ Parser handles multi-line comma-separated input
- ✅ Test infrastructure is ready
- ✅ Example data is extracted and accessible

---

## Phase 2: Pattern Detection Core (Part 1)

**Goal**: Implement the core pattern detection for exact double repetition.

### Tasks

#### 2.1 Pattern Detection Algorithm

- **Function**: `is_invalid_part1(product_id: int) -> bool`
- **Purpose**: Detect if an ID is formed by a sequence repeated exactly twice
- **Algorithm**:
  1. Convert ID to string
  2. Check lengths from 1 to len(str)//2
  3. For each potential sequence length:
     - Split ID string in half
     - Compare first half to second half
     - If equal, return True
  4. Return False if no match found
- **Optimization**: Only need to check if length is even and divisible by 2
- **Edge Cases**:
  - Single-digit numbers (cannot be invalid)
  - Odd-length numbers (cannot be exact double)

#### 2.2 Range Processing

- **Function**: `find_invalid_ids_in_range(start: int, end: int, validator: Callable) -> List[int]`
- **Purpose**: Find all invalid IDs within a given range using provided validator
- **Implementation**:
  - Iterate from start to end (inclusive)
  - Apply validator function to each ID
  - Collect all invalid IDs
  - Return list
- **Design Note**: Accepts validator as parameter for reusability in Part 2

#### 2.3 Sum Calculation

- **Function**: `calculate_invalid_sum(ranges: List[Tuple[int, int]], validator: Callable) -> int`
- **Purpose**: Calculate sum of all invalid IDs across all ranges
- **Implementation**:
  - Process each range with find_invalid_ids_in_range
  - Sum all collected invalid IDs
  - Return total sum

### Acceptance Criteria

- ✅ `is_invalid_part1(11)` returns `True`
- ✅ `is_invalid_part1(1010)` returns `True`
- ✅ `is_invalid_part1(123123)` returns `True`
- ✅ `is_invalid_part1(101)` returns `False`
- ✅ `is_invalid_part1(111)` returns `False` (not exact double)
- ✅ Example input produces sum of `1227775554`

---

## Phase 3: Unit Tests for Part 1

**Goal**: Comprehensive test coverage for Part 1 functionality.

### Tasks

#### 3.1 Pattern Detection Tests

- Test valid invalid IDs: `11`, `22`, `99`, `1010`, `6464`, `123123`, `1188511885`, `222222`, `446446`, `38593859`
- Test valid IDs (not invalid): `101`, `111`, `123`, `1234`, `99999`
- Test single-digit IDs: `1`, `5`, `9`
- Test edge cases: minimum invalid (`11`), large IDs

#### 3.2 Range Processing Tests

- Test each example range individually (AC-101 through AC-109)
- Verify correct invalid IDs found per range
- Test empty ranges (no invalid IDs)
- Test single-element ranges

#### 3.3 Integration Tests

- Test complete example input (AC-110)
- Test with actual puzzle input
- Performance test with large ranges

### Acceptance Criteria

- ✅ All unit tests pass
- ✅ All acceptance criteria (AC-101 through AC-110) validated
- ✅ Edge cases covered

---

## Phase 4: Extended Pattern Detection (Part 2)

**Goal**: Extend pattern detection to handle multiple repetitions (2 or more).

### Tasks

#### 4.1 Enhanced Pattern Detection

- **Function**: `is_invalid_part2(product_id: int) -> bool`
- **Purpose**: Detect if an ID is formed by a sequence repeated 2+ times
- **Algorithm**:
  1. Convert ID to string
  2. For each potential sequence length (1 to len(str)//2):
     - Check if len(str) is divisible by sequence length
     - Extract the candidate sequence (first N characters)
     - Verify the entire string is this sequence repeated
     - If yes, check if repetition count ≥ 2
     - If match, return True
  3. Return False if no match found
- **Key Difference from Part 1**: Accepts any repetition count ≥ 2, not just exactly 2

#### 4.2 Optimization Considerations

- **Challenge**: Ranges can contain millions of IDs
- **Strategy**:
  - Direct iteration acceptable for reasonable ranges
  - Mathematical generation not feasible (no clear formula)
  - Focus on efficient per-ID validation
- **Pattern Detection Optimization**:
  - Early termination when match found
  - Only check divisors of string length
  - String comparison is fast for small sequences

#### 4.3 Code Reuse

- **Shared Function**: `find_invalid_ids_in_range` already accepts validator parameter
- **Shared Function**: `calculate_invalid_sum` already accepts validator parameter
- **New**: Create `solve_part1()` and `solve_part2()` wrapper functions
- **Pattern**: Pass appropriate validator to shared calculation logic

### Acceptance Criteria

- ✅ `is_invalid_part2(11)` returns `True`
- ✅ `is_invalid_part2(111)` returns `True`
- ✅ `is_invalid_part2(1010)` returns `True`
- ✅ `is_invalid_part2(123123123)` returns `True`
- ✅ `is_invalid_part2(565656)` returns `True`
- ✅ `is_invalid_part2(101)` returns `False`
- ✅ All Part 1 invalid IDs remain invalid in Part 2

---

## Phase 5: Unit Tests for Part 2

**Goal**: Comprehensive test coverage for Part 2 functionality.

### Tasks

#### 5.1 Pattern Detection Tests

- Test all Part 1 invalid IDs (should still be invalid)
- Test new invalid patterns: `111`, `999`, `123123123`, `1212121212`, `1111111`, `565656`, `824824824`, `2121212121`
- Test IDs that are invalid in Part 2 but not Part 1
- Test valid IDs that have repetitions but don't qualify

#### 5.2 Range Processing Tests

- Test each example range individually (AC-201 through AC-211)
- Verify additional invalid IDs found in Part 2
- Compare Part 1 vs Part 2 results for same ranges
- Ensure Part 2 is superset of Part 1 results

#### 5.3 Integration Tests

- Test complete example input (AC-212)
- Verify sum equals `4174379265`
- Test with actual puzzle input
- Performance validation

### Acceptance Criteria

- ✅ All unit tests pass
- ✅ All acceptance criteria (AC-201 through AC-212) validated
- ✅ Part 2 sum includes all Part 1 invalid IDs plus additional ones
- ✅ Example produces correct sum: `4174379265`

---

## Phase 6: Edge Cases & Validation

**Goal**: Handle edge cases and validate robustness.

### Tasks

#### 6.1 Leading Zero Handling

- **Test**: Confirm `0101` is not considered a valid product ID
- **Test**: Confirm `101` is evaluated correctly
- **Note**: Input parsing already converts to integers (no leading zeros possible)
- **Validation**: Document that integer conversion handles this automatically

#### 6.2 Boundary Conditions

- **Empty ranges**: start > end
- **Single-element ranges**: start == end
- **Single-digit ranges**: e.g., `1-9`
- **Large ID ranges**: Test performance with millions of IDs
- **Very large IDs**: Test with IDs in billions

#### 6.3 Edge Case Tests

- Ranges with no invalid IDs (contribution = 0)
- All ranges empty (total sum = 0)
- Single range with all invalid IDs
- Mixed ranges (some with, some without invalid IDs)

### Acceptance Criteria

- ✅ All edge case acceptance criteria (AC-301 through AC-305) pass
- ✅ No integer overflow for large sums
- ✅ Performance acceptable for large ranges
- ✅ Graceful handling of edge inputs

---

## Phase 7: Integration & Documentation

**Goal**: Complete solution with proper structure and documentation.

### Tasks

#### 7.1 Main Entry Point

- **File**: `agent.py`
- **Functions**:
  - `solve_part1(input_text: str) -> int`
  - `solve_part2(input_text: str) -> int`
  - `main()` - reads input file and prints both answers

#### 7.2 Code Organization

- **Module structure**:
  ```python
  # agent.py
  # - Input parsing functions
  # - Pattern detection functions (part 1 & 2)
  # - Range processing functions
  # - Solution wrapper functions
  # - Main entry point
  ```

#### 7.3 Documentation

- **Docstrings**: Add comprehensive docstrings to all functions
- **Comments**: Explain pattern detection algorithms
- **Type hints**: Use throughout for clarity
- **Examples**: Include example usage in docstrings

#### 7.4 Final Validation

- Run complete test suite
- Validate against example input
- Run against actual puzzle input
- Verify both Part 1 and Part 2 answers

### Acceptance Criteria

- ✅ All tests pass
- ✅ Code is well-documented
- ✅ Solution produces correct answers for both parts
- ✅ Code follows Python best practices

---

## Implementation Details

### Data Structures

```python
# Input representation
Range = Tuple[int, int]  # (start, end) inclusive
Ranges = List[Range]

# Validator function type
Validator = Callable[[int], bool]
```

### Core Algorithm Complexity

- **Pattern Detection (Part 1)**: O(log n) where n is number of digits

  - Only checks exact half-point split
  - Constant for most practical IDs

- **Pattern Detection (Part 2)**: O(d²) where d is number of digits

  - Checks all divisors of string length
  - Bounded by small digit count (even billions = 10 digits)

- **Range Processing**: O(r \* p) where r is range size, p is pattern check time

  - Linear scan through range required (no mathematical shortcut)
  - Per-ID validation is fast (< 100 operations)

- **Overall**: O(n \* d²) where n is total IDs across all ranges
  - Efficient for typical Advent of Code input sizes

### Performance Considerations

- **String operations**: Fast for small strings (< 20 characters typical)
- **No premature optimization**: Focus on correctness first
- **If needed**: Can optimize with mathematical patterns or parallel processing
- **Expected**: Standard Python implementation should handle AoC inputs efficiently

---

## Testing Strategy

### Test Organization

```python
# test_day2.py structure
class TestInputParsing:
    # Input parsing tests

class TestPatternDetectionPart1:
    # Part 1 validation tests

class TestRangeProcessingPart1:
    # Part 1 range tests

class TestPart1Integration:
    # Part 1 end-to-end tests

class TestPatternDetectionPart2:
    # Part 2 validation tests

class TestRangeProcessingPart2:
    # Part 2 range tests

class TestPart2Integration:
    # Part 2 end-to-end tests

class TestEdgeCases:
    # Edge case validation
```

### Example Test Data

```python
EXAMPLE_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

PART1_EXPECTED_SUM = 1227775554
PART2_EXPECTED_SUM = 4174379265

# Individual range expected results...
```

---

## Risk Assessment

### Identified Risks

1. **Performance Risk**: Large ranges (millions of IDs)

   - **Mitigation**: Efficient per-ID validation, early testing with large ranges
   - **Fallback**: Optimize or parallelize if needed

2. **Integer Overflow**: Very large sums

   - **Mitigation**: Python handles arbitrary precision integers natively
   - **Validation**: Test with known large sums

3. **Pattern Detection Bugs**: Complex repetition logic

   - **Mitigation**: Comprehensive unit tests for all pattern types
   - **Validation**: Test against all spec examples

4. **Off-by-One Errors**: Inclusive range handling
   - **Mitigation**: Clear documentation, explicit tests for boundaries
   - **Validation**: Test ranges where boundaries are invalid IDs

### Contingency Plans

- If performance inadequate: Profile and optimize hot paths
- If pattern detection flawed: Add more test cases, review algorithm
- If Part 2 breaks Part 1: Ensure validators are independent

---

## Definition of Done

### Phase Completion Criteria

- [ ] Phase 1: Input parser handles all test cases
- [ ] Phase 2: Part 1 pattern detection correct for all examples
- [ ] Phase 3: All Part 1 tests pass
- [ ] Phase 4: Part 2 pattern detection correct for all examples
- [ ] Phase 5: All Part 2 tests pass
- [ ] Phase 6: All edge cases handled
- [ ] Phase 7: Complete, documented, validated solution

### Overall Success Criteria

- [ ] Example input produces correct Part 1 sum: `1227775554`
- [ ] Example input produces correct Part 2 sum: `4174379265`
- [ ] All acceptance criteria (AC-101 through AC-305) pass
- [ ] All validation criteria (VAL-001 through VAL-006) pass
- [ ] Actual puzzle input produces accepted answers
- [ ] Code is clean, documented, and maintainable
- [ ] No known bugs or edge case failures

---

## Next Steps

1. **Begin Phase 1**: Set up input parsing and test infrastructure
2. **Validate early**: Test parser with example input immediately
3. **Iterate quickly**: Move through phases systematically
4. **Test continuously**: Run tests after each function implementation
5. **Refactor as needed**: Keep code clean and simple throughout

---

## Notes

- **No main.py reference**: Solution developed independently per agent instructions
- **Focus on reusability**: Part 2 reuses Part 1 infrastructure with different validator
- **Performance-conscious**: Design for efficiency but prioritize correctness
- **Test-driven**: Write tests alongside implementation for confidence
- **Simplicity first**: Don't over-engineer; solve the problem directly

---

**Plan Status**: Ready for Implementation  
**Estimated Effort**: 4-6 hours  
**Complexity**: Medium (pattern matching, large ranges)
