# AOC2025

Advent of code 2025 - python & agent follow up

- Each day I'll have a `main.py` file with my attempt at solving the problem in python without any AI Agent help. There may also be supporting files that aren't `AI` related, but won't be specified here.
- Then, I'll have an agent version, `agent.py`, that uses an AI agent workflow to help solve the problem.
  - The agent workflow will follow a spec-driven approach where I work with the agent to define the requirements and spec for the solution, come up with a phased plan, then execute that plan.
  - The agent will leverage three custom chatmodes defined in the .github/chatmodes folder:
    - plan.chatmode.md - for planning and strategizing implementation
    - spec.chatmode.md - for generating specification documents
    - implementation.chatmode.md - for implementing code based on the spec and plan
  - Refer to the implementation-summary.md file in the `context/` folder of each day for details on how the agent implemented the solution.

## [Day 1: Secret Entrance](https://adventofcode.com/2025/day/1)

- [Python](day1/main.py)
- [Agent](day1/agent.py)
