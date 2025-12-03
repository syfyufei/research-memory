---
description: Query research memory history
---

Use the research-memory skill to search through project history.

Ask the user what they want to search for if not specified.

Call the `research_memory_query_history` tool with the search query to find relevant information from:
- Development logs (`memory/devlog.md`)
- Decision records (`memory/decisions.md`)
- Experiment data (`memory/experiments.csv`)

Present the search results with context, timestamps, and relevant excerpts.
