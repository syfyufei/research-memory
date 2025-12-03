# Slash Commands Reference

Complete guide to all Research Memory slash commands.

## Overview

Research Memory provides 10 slash commands organized into two categories:

- **Core Commands**: Essential daily operations
- **Analysis & Reporting**: Advanced analysis and insights

All commands can also be triggered via natural language.

---

## Core Commands

### `/research-memory:bootstrap`
**Restore project context and generate work plan**

Loads your project overview, recent work, and TODO list to help you quickly resume where you left off.

**What it does:**
- Reads `memory/project-overview.md` for project context
- Shows last 5 development log entries from `memory/devlog.md`
- Lists open TODOs from `memory/todos.md`
- Suggests next steps based on current state

**When to use:**
- Starting a new work session
- After being away from the project
- Beginning of the day/week

**Example usage:**
```bash
/research-memory:bootstrap
```

**Natural language:**
```
"Research Memory, help me get back up to speed with my project"
"Bootstrap my project context"
"What did I work on last?"
```

---

### `/research-memory:status`
**Quick project status overview**

Shows a compact dashboard-style summary of your project's current state.

**What it displays:**
- Project name and objective
- Last update timestamp
- Recent progress (1-2 line summary)
- Current research phase
- TODO statistics (open vs completed)
- Quick stats (sessions logged, experiments, decisions)

**When to use:**
- Quick check-in on project health
- Before meetings or standups
- Monitoring progress velocity

**Example usage:**
```bash
/research-memory:status
```

**Natural language:**
```
"Show me a quick status of the project"
"What's the current state?"
"Quick project overview"
```

---

### `/research-memory:focus`
**Get focused daily work plan**

Generates a prioritized, actionable plan for today based on your TODOs, recent work, and project dependencies.

**What it provides:**
- **Top Priority**: Single most important task (2-3 hours)
  - Why it's urgent
  - What it blocks
  - Success criteria
- **Secondary Tasks**: 2-3 important tasks (1-2 hours each)
- **Stretch Goals**: Nice-to-have tasks for extra time
- **Time Budget**: Realistic time allocation
- **Focus Recommendations**: Specific advice on task order and approach
- **Not Today**: Important tasks that should wait

**Selection criteria:**
1. Tasks blocking other work
2. Urgent/time-sensitive items
3. Dependencies for planned work
4. Energy level optimization
5. Momentum building

**Optional arguments:**
- `--hours N` : Plan for N hours (default: 6-8)
- `--energy high|normal|low` : Adjust for energy level
- `--mode deep|varied|quick` : Focus style

**When to use:**
- Start of workday
- When feeling overwhelmed
- After completing a major task
- When priorities are unclear

**Example usage:**
```bash
/research-memory:focus
/research-memory:focus --hours 4
/research-memory:focus --energy low --mode quick
```

**Example output:**
```
☀️ Today's Focus (Dec 3, 2025)

⚡ Top Priority (2-3 hours):
• Fix heteroscedasticity in baseline model
  → Blocks: robustness tests, paper writing
  → Context: Found issue yesterday, need log transformation
  → Success: Breusch-Pagan test p > 0.05

📌 Secondary Tasks (1-2 hours each):
• Add 3 control variables to model (Est: 1.5h | Impact: High)
• Update experiment documentation (Est: 1h | Impact: Medium)

🎯 Stretch Goals (if time permits):
• Start drafting results section

💡 Recommendation: Focus on fixing heteroscedasticity first.
   Everything else depends on it! Use deep work block (90-120 min).
```

**Natural language:**
```
"What should I focus on today?"
"Give me a daily work plan"
"Help me prioritize my tasks"
"What's the most important thing to do now?"
```

---

### `/research-memory:remember`
**Remember current work session**

Analyzes the conversation and logs structured information to memory files.

**What it captures:**
- Session goal and objectives
- Summary of changes made
- Experiments conducted (hypothesis, dataset, model, metrics)
- Key decisions (rationale and alternatives)
- New and completed TODOs
- Research phase indicators

**What it updates:**
- `memory/devlog.md` - Timestamped session log
- `memory/experiments.csv` - Structured experiment records
- `memory/decisions.md` - Decision documentation
- `memory/todos.md` - TODO list updates

**When to use:**
- End of work session
- After completing major milestones
- Before switching to another project

**Example usage:**
```bash
/research-memory:remember
```

**Natural language:**
```
"Remember this work session"
"Log today's work to research memory"
"Record this session"
```

---

### `/research-memory:query`
**Query research memory history**

Searches across all memory files for relevant historical information.

**What it searches:**
- `memory/devlog.md` - Development logs
- `memory/decisions.md` - Decision records
- `memory/experiments.csv` - Experiment data

**What you get:**
- Relevant excerpts with context
- Timestamps for each match
- Research phase information

**When to use:**
- Finding past decisions
- Reviewing experiment results
- Checking why something was done

**Example usage:**
```bash
/research-memory:query
# Claude will ask: "What would you like to search for?"
```

**Natural language:**
```
"Search for our decisions about spatial lag models"
"Why did we choose log transformation?"
"Find experiments related to heteroscedasticity"
```

---

## Analysis & Reporting Commands

### `/research-memory:timeline`
**Visualize project timeline**

Creates a chronological timeline of all project activities with emoji indicators.

**What it shows:**
- 📊 Data processing activities
- 🔬 Experiments conducted
- 🤔 Decisions made
- ✅ Completed milestones
- 📝 Writing progress

**Optional arguments:**
- `--last 7d` : Show last 7 days
- `--last 30d` : Show last 30 days
- `--from YYYY-MM-DD --to YYYY-MM-DD` : Custom date range
- Default: Last 14 days

**When to use:**
- Visualizing project progress
- Identifying productivity patterns
- Preparing progress reports

**Example usage:**
```bash
/research-memory:timeline
/research-memory:timeline --last 30d
/research-memory:timeline --from 2025-11-01 --to 2025-11-30
```

**Example output:**
```
2025-11-15 | 📊 [DATA] Data cleaning completed - removed 150 outliers
2025-11-18 | 🔬 [MODEL] Baseline model R²=0.72
2025-11-20 | 🤔 [DECISION] Chose log transformation over Box-Cox
2025-11-22 | ✅ [ROBUST] Heteroscedasticity test passed
```

---

### `/research-memory:summary`
**Generate comprehensive project summary**

Creates a polished, structured summary of the entire project suitable for presentations and reports.

**What it includes:**
- **Project Overview**: Research questions, hypotheses, timeline
- **Key Findings**: Successful experiments with metrics
- **Important Decisions**: Major decisions with rationale
- **Progress Summary**: Completed/in-progress/planned phases
- **Open Questions**: Outstanding issues and next steps

**When to use:**
- Preparing for advisor meetings
- Team updates and presentations
- Documentation for papers
- Progress reports

**Example usage:**
```bash
/research-memory:summary
```

**Natural language:**
```
"Generate a project summary for my weekly meeting"
"Create a comprehensive summary of this project"
"Prepare a report of all our work"
```

---

### `/research-memory:review`
**Review work in a specific time period**

Generates a structured review of activities within a specified timeframe.

**What it provides:**
- Activity summary (sessions, experiments, decisions, TODOs)
- Detailed week-by-week breakdown
- Key achievements
- Challenges and how they were resolved
- Productivity insights (most productive days, focus areas)

**Optional arguments:**
- `--last-week` : Review last 7 days
- `--last-month` : Review last 30 days
- `--from YYYY-MM-DD --to YYYY-MM-DD` : Custom range
- `--format report|weekly|monthly` : Different report styles

**When to use:**
- Weekly/monthly retrospectives
- Performance reviews
- Identifying bottlenecks
- Planning future work

**Example usage:**
```bash
/research-memory:review --last-week
/research-memory:review --from 2025-11-01 --to 2025-11-30
```

---

### `/research-memory:insights`
**Get AI-powered insights and suggestions**

Analyzes all memory files and provides intelligent recommendations.

**What it analyzes:**
- 🔍 **Pattern Analysis**: Work habits, research phases, iteration speed
- ⚠️ **Potential Issues**: Forgotten TODOs, stale decisions, repeated experiments
- 💡 **Suggestions**: Next steps, quick wins, research directions
- 📊 **Project Health**: Momentum, clarity, documentation quality
- 🎯 **Recommendations**: 3-5 prioritized actionable items

**When to use:**
- When feeling stuck
- Planning next phase
- Looking for optimization opportunities
- Periodic project health checks

**Example usage:**
```bash
/research-memory:insights
```

**Natural language:**
```
"Analyze my project and give me insights"
"What should I focus on next?"
"Are there any issues I should address?"
```

---

### `/research-memory:checkpoint`
**Create a named checkpoint of current state**

Captures a snapshot of your project state at important milestones.

**What it records:**
- Checkpoint name and timestamp
- Current research phase
- Project state summary
- Open TODOs count
- Recent experiments
- Key metrics snapshot
- Important context notes

**Saved to:** `memory/checkpoints.md`

**Optional tags:**
- `--tag milestone` : Mark as project milestone
- `--tag experiment` : Mark as experiment checkpoint
- `--tag backup` : Mark as safety backup

**When to use:**
- Before major changes or refactors
- At paper draft milestones
- When finalizing experiments
- End of development sprints

**Example usage:**
```bash
/research-memory:checkpoint "Paper draft v1 complete"
/research-memory:checkpoint "Baseline model finalized" --tag experiment
/research-memory:checkpoint "Before refactor" --tag backup
```

**Natural language:**
```
"Create a checkpoint called 'baseline complete'"
"Save the current state as a milestone"
```

---

## Command Comparison

| Command | Use Case | Output | Updates Files |
|---------|----------|--------|---------------|
| `bootstrap` | Resume work | Context summary + plan | No |
| `status` | Quick check | Compact dashboard | No |
| `focus` | Daily planning | Prioritized task list | No |
| `remember` | Log session | Confirmation message | Yes (all) |
| `query` | Find info | Search results | No |
| `timeline` | Visualize progress | Chronological view | No |
| `summary` | Full report | Comprehensive doc | No |
| `review` | Retrospective | Period analysis | No |
| `insights` | Get suggestions | AI recommendations | No |
| `checkpoint` | Save milestone | Checkpoint created | Yes (checkpoints.md) |

---

## Tips & Best Practices

### Daily Workflow
1. **Start of day**: `/research-memory:bootstrap` or `/research-memory:focus`
2. **Quick check**: `/research-memory:status`
3. **End of day**: `/research-memory:remember`

**Pro tip**: Use `bootstrap` when you need context, use `focus` when you know the context but need to prioritize.

### Weekly Review
1. **Review week**: `/research-memory:review --last-week`
2. **Check insights**: `/research-memory:insights`
3. **Plan ahead**: Use insights to guide next week

### Before Important Meetings
1. **Generate summary**: `/research-memory:summary`
2. **Check timeline**: `/research-memory:timeline --last 30d`
3. **Review milestones**: Check `memory/checkpoints.md`

### When Stuck
1. **Get insights**: `/research-memory:insights`
2. **Review past decisions**: `/research-memory:query`
3. **Check timeline**: `/research-memory:timeline`

---

## Natural Language Triggers

All commands can be triggered with natural language. Examples:

**Bootstrap:**
- "Help me get back up to speed"
- "What was I working on?"
- "Restore my project context"

**Status:**
- "Show me project status"
- "Quick overview please"
- "How's the project doing?"

**Focus:**
- "What should I focus on today?"
- "Give me a daily work plan"
- "Help me prioritize my tasks"
- "What's most important right now?"

**Remember:**
- "Remember this session"
- "Log today's work"
- "Save this to research memory"

**Query:**
- "Why did we choose [approach]?"
- "Find experiments about [topic]"
- "Search for decisions related to [X]"

**Timeline:**
- "Show me what I've been working on"
- "Timeline for the past month"
- "Visualize my progress"

**Summary:**
- "Generate a project summary"
- "Prepare a report for my meeting"
- "Summarize everything we've done"

**Review:**
- "Review last week's work"
- "What did I accomplish this month?"
- "Analyze my productivity"

**Insights:**
- "Give me some insights"
- "What should I focus on?"
- "Analyze my project"

**Checkpoint:**
- "Create a checkpoint"
- "Save this milestone"
- "Mark this as a backup point"

---

## Command History & Evolution

**v0.4.0** (Current)
- ✨ Added `/focus` command for daily work planning
- 🎯 Enhanced task prioritization and time management

**v0.3.0**
- ✨ Added 6 new commands (status, timeline, summary, review, insights, checkpoint)
- 📝 Renamed `/log` to `/remember` for clarity
- 🎯 Organized into Core and Analysis categories

**v0.2.0**
- Initial slash commands (bootstrap, log, query)
- Natural language support

**v0.1.0**
- Skill-only (no slash commands)

---

## See Also

- [Installation Guide](../README.md#installation)
- [Architecture Overview](../README.md#architecture-overview)
- [Contributing](../CONTRIBUTING.md)
