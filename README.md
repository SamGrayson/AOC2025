# AOC2025

Advent of code 2025 - python & agent follow up

- Each day I'll have a folder with my attempt at solving the problem in python without any AI Agent help.
- Then, I'll have an agent version that uses an AI agent to help solve the problem.
  - The agent flow will follow a spec-driven approach where I work with the agent to define the requirements and spec for the solution, come up with a phased plan, then execute that plan.
  - The agent will leverage two custom agents defined in the .github/agents folder:
    - plan.agent.md - for planning and strategizing implementation
    - spec.agent.md - for generating specification documents
    - implementation.agent.md - for implementing code based on the spec and plan
    - Refer to the implementation-summary.md file in the `context/` folder of each day for details on how the agent implemented the solution.

## [Day 1: Secret Entrance](https://adventofcode.com/2025/day/1)

- [Python](day1/main.py)
- [Agent](day1/agent.py)
