---
title: Invalid Product ID Detection and Summation
version: 1.0
date_created: 2025-12-02
last_updated: 2025-12-02
owner: Advent of Code 2025 - Day 2
tags: [design, pattern-matching, validation, advent-of-code]
---

# Introduction

This specification defines the requirements for identifying and summing invalid product IDs within specified ranges. The gift shop database contains product ID ranges that may include invalid IDs following specific patterns. The solution must identify these invalid IDs according to defined rules and calculate their sum.

## 1. Purpose & Scope

**Purpose**: Define the requirements for detecting invalid product IDs within given ranges and calculating the sum of all invalid IDs found.

**Scope**: This specification covers:

- Parsing product ID ranges from input format
- Identifying invalid product IDs based on pattern-matching rules
- Calculating the sum of all invalid IDs across all ranges
- Two distinct validation rules (Part 1 and Part 2)

**Intended Audience**: AI agents and developers implementing the solution.

**Assumptions**:

- Input is provided as a single line or multiple lines containing comma-separated ranges
- Each range is well-formed with valid start and end values
- All product IDs are positive integers
- No product IDs have leading zeroes

## 2. Definitions

- **Product ID**: A positive integer representing a unique product identifier
- **Product ID Range**: A pair of integers representing the inclusive start and end of a contiguous sequence of product IDs, formatted as `start-end`
- **Invalid ID**: A product ID that matches specific pattern-based criteria for invalidity
- **Repeated Sequence Pattern**: A digit sequence that appears consecutively multiple times to form the complete number
- **Leading Zero**: A zero digit at the beginning of a number representation (e.g., 0101, 001)

## 3. Requirements, Constraints & Guidelines

### Input Processing Requirements

- **REQ-001**: The system shall accept input containing one or more product ID ranges
- **REQ-002**: Ranges shall be separated by commas (`,`)
- **REQ-003**: Each range shall be formatted as `start-end` where start and end are positive integers
- **REQ-004**: The system shall parse ranges that may appear across multiple lines or on a single line
- **REQ-005**: Both start and end values in a range are inclusive

### Part 1: Invalid ID Detection (Exact Double Repetition)

- **REQ-101**: An ID is invalid if it consists of a digit sequence repeated exactly twice
- **REQ-102**: The repeated sequence must form the entire ID with no additional digits
- **REQ-103**: Valid examples of invalid IDs under this rule:
  - `11` (digit 1 repeated twice)
  - `22` (digit 2 repeated twice)
  - `99` (digit 9 repeated twice)
  - `1010` (sequence "10" repeated twice)
  - `6464` (sequence "64" repeated twice)
  - `123123` (sequence "123" repeated twice)
  - `1188511885` (sequence "118851188" repeated twice)
  - `222222` (sequence "222" repeated twice)
  - `446446` (sequence "446" repeated twice)
  - `38593859` (sequence "3859" repeated twice)

### Part 2: Invalid ID Detection (Multiple Repetitions)

- **REQ-201**: An ID is invalid if it consists of a digit sequence repeated at least twice (2 or more times)
- **REQ-202**: The repeated sequence must form the entire ID with no additional digits
- **REQ-203**: This rule includes all IDs from Part 1 plus additional patterns with 3+ repetitions
- **REQ-204**: Valid examples of invalid IDs under this rule:
  - All examples from REQ-103 remain invalid
  - `111` (digit "1" repeated three times)
  - `999` (digit "9" repeated three times)
  - `12341234` (sequence "1234" repeated twice)
  - `123123123` (sequence "123" repeated three times)
  - `1212121212` (sequence "12" repeated five times)
  - `1111111` (digit "1" repeated seven times)
  - `565656` (sequence "56" repeated three times)
  - `824824824` (sequence "824" repeated three times)
  - `2121212121` (sequence "21" repeated five times)

### Validation Constraints

- **CON-001**: Numbers with leading zeroes (e.g., 0101) are not valid product IDs and shall be ignored
- **CON-002**: An ID without leading zeroes (e.g., 101) is a valid ID format that shall be evaluated against the invalidity rules
- **CON-003**: An invalid ID must be formed by an exact repetition with no remainder digits
- **CON-004**: Single-digit IDs cannot be invalid under Part 1 rules (minimum invalid ID is 11)
- **CON-005**: Single-digit IDs cannot be invalid under Part 2 rules (minimum invalid ID is 11)

### Output Requirements

- **REQ-301**: The system shall calculate the sum of all invalid IDs found across all ranges
- **REQ-302**: The output shall be a single integer representing this sum
- **REQ-303**: If no invalid IDs are found, the sum shall be zero

### Performance Expectations

- **PER-001**: The system must handle ranges with millions of IDs efficiently
- **PER-002**: The system must handle very large product IDs (up to billions)

**Quality Expectations:**

- **QE-001**: Solution must produce correct results for all valid inputs
- **QE-002**: Solution must correctly identify all invalid IDs according to the specified rules
- **QE-003**: Solution must accurately sum all invalid IDs without overflow or precision loss
- **QE-004**: Solution must handle edge cases such as empty ranges or ranges with no invalid IDs
- **QE-005**: Solution must distinguish between Part 1 and Part 2 validation rules

## 4. Acceptance Criteria

### Part 1 Acceptance Criteria

**Example Input:**

```
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
```

- **AC-101**: Given the range `11-22`, When evaluated under Part 1 rules, Then the invalid IDs found shall be `11` and `22`
- **AC-102**: Given the range `95-115`, When evaluated under Part 1 rules, Then the invalid ID found shall be `99`
- **AC-103**: Given the range `998-1012`, When evaluated under Part 1 rules, Then the invalid ID found shall be `1010`
- **AC-104**: Given the range `1188511880-1188511890`, When evaluated under Part 1 rules, Then the invalid ID found shall be `1188511885`
- **AC-105**: Given the range `222220-222224`, When evaluated under Part 1 rules, Then the invalid ID found shall be `222222`
- **AC-106**: Given the range `1698522-1698528`, When evaluated under Part 1 rules, Then no invalid IDs shall be found
- **AC-107**: Given the range `446443-446449`, When evaluated under Part 1 rules, Then the invalid ID found shall be `446446`
- **AC-108**: Given the range `38593856-38593862`, When evaluated under Part 1 rules, Then the invalid ID found shall be `38593859`
- **AC-109**: Given the ranges `565653-565659`, `824824821-824824827`, and `2121212118-2121212124`, When evaluated under Part 1 rules, Then no invalid IDs shall be found
- **AC-110**: Given the complete example input, When all invalid IDs are summed under Part 1 rules, Then the result shall be `1227775554`

### Part 2 Acceptance Criteria

**Example Input:** (same as Part 1)

- **AC-201**: Given the range `11-22`, When evaluated under Part 2 rules, Then the invalid IDs found shall be `11` and `22`
- **AC-202**: Given the range `95-115`, When evaluated under Part 2 rules, Then the invalid IDs found shall be `99` and `111`
- **AC-203**: Given the range `998-1012`, When evaluated under Part 2 rules, Then the invalid IDs found shall be `999` and `1010`
- **AC-204**: Given the range `1188511880-1188511890`, When evaluated under Part 2 rules, Then the invalid ID found shall be `1188511885`
- **AC-205**: Given the range `222220-222224`, When evaluated under Part 2 rules, Then the invalid ID found shall be `222222`
- **AC-206**: Given the range `1698522-1698528`, When evaluated under Part 2 rules, Then no invalid IDs shall be found
- **AC-207**: Given the range `446443-446449`, When evaluated under Part 2 rules, Then the invalid ID found shall be `446446`
- **AC-208**: Given the range `38593856-38593862`, When evaluated under Part 2 rules, Then the invalid ID found shall be `38593859`
- **AC-209**: Given the range `565653-565659`, When evaluated under Part 2 rules, Then the invalid ID found shall be `565656`
- **AC-210**: Given the range `824824821-824824827`, When evaluated under Part 2 rules, Then the invalid ID found shall be `824824824`
- **AC-211**: Given the range `2121212118-2121212124`, When evaluated under Part 2 rules, Then the invalid ID found shall be `2121212121`
- **AC-212**: Given the complete example input, When all invalid IDs are summed under Part 2 rules, Then the result shall be `4174379265`

### Edge Case Acceptance Criteria

- **AC-301**: Given an ID with leading zeroes (e.g., `0101`), When evaluated, Then it shall not be considered a valid product ID
- **AC-302**: Given an ID without leading zeroes (e.g., `101`), When evaluated, Then it shall be checked against the invalidity rules
- **AC-303**: Given a range with no invalid IDs, When evaluated, Then the contribution to the sum shall be zero
- **AC-304**: Given single-digit IDs, When evaluated, Then they shall not be considered invalid under either rule set
- **AC-305**: Given very large product IDs (billions), When evaluated, Then they shall be processed correctly without overflow

## 5. Rationale & Context

**Pattern Recognition**: The invalid ID patterns represent "silly patterns" created by a young Elf, specifically numbers formed by repeating digit sequences. Part 1 focuses on exact double repetitions (the most obvious pattern), while Part 2 expands to include any number of repetitions (2 or more).

**Leading Zeroes Constraint**: Leading zeroes are explicitly disallowed because they don't represent valid product IDs in typical database systems. This prevents ambiguity between octal and decimal representations.

**Inclusive Ranges**: Both endpoints of a range are inclusive, meaning the range `11-22` includes both 11 and 22 as potential product IDs.

**Summation Requirement**: The final output is a sum rather than a count or list, providing a single numerical answer that can be easily verified.

**Two-Part Structure**: Part 1 establishes the basic pattern detection capability (exact double repetition), while Part 2 extends it to detect a broader class of patterns (any repetition count ≥ 2), testing the solution's flexibility.

## 6. Validation Criteria

The solution shall be validated by:

- **VAL-001**: Confirming the Part 1 example produces the sum `1227775554`
- **VAL-002**: Confirming the Part 2 example produces the sum `4174379265`
- **VAL-003**: Verifying each individual range from the examples produces the expected invalid IDs
- **VAL-004**: Testing edge cases including:
  - Empty ranges (start > end)
  - Single-element ranges (start == end)
  - Ranges containing only valid IDs
  - Ranges with very large product IDs
  - Single-digit ranges
- **VAL-005**: Confirming that leading zero handling is correct
- **VAL-006**: Verifying that the pattern detection correctly identifies repetitions of various lengths

## 7. Related Specifications / Further Reading

- [Advent of Code 2025 - Day 2](https://adventofcode.com/2025/day/2)
- [Pattern Matching in Numeric Sequences](https://en.wikipedia.org/wiki/Pattern_matching)
- [Integer Overflow Considerations](https://en.wikipedia.org/wiki/Integer_overflow)
