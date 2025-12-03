---
description: Review work in a specific time period
---

Use the research-memory skill to review work done in a specific time period.

Ask the user for the time period if not specified in the command arguments.

Read from memory files and extract all activities within the specified period:
- Development log entries
- Experiments conducted
- Decisions made
- TODOs created and completed

Present as a structured review:

## Period Review: [START_DATE] to [END_DATE]

### Summary
- Total sessions: X
- Experiments completed: Y
- Decisions made: Z
- TODOs completed: N of M

### Detailed Activities

#### Week of [DATE]
- [Activity 1 with context]
- [Activity 2 with context]

#### Week of [DATE]
- [Activity 1 with context]
- [Activity 2 with context]

### Key Achievements
- [Notable accomplishment 1]
- [Notable accomplishment 2]

### Challenges & Blockers
- [Issue 1 and how it was resolved]
- [Issue 2 and current status]

### Productivity Insights
- Most productive days: [DAYS]
- Primary focus area: [PHASE]
- Velocity: X activities per week

Support arguments:
- `--last-week` : Review last 7 days
- `--last-month` : Review last 30 days
- `--from YYYY-MM-DD --to YYYY-MM-DD` : Custom range
- `--format report|weekly|monthly` : Different report styles
