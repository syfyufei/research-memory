---
description: Get focused daily work plan
---

Use the research-memory skill to generate a focused daily work plan.

Read from memory files and analyze:
- Open TODOs from `memory/todos.md`
- Recent work context from `memory/devlog.md`
- Current project phase and blockers
- Dependencies between tasks

Generate a focused daily plan with:

## ☀️ Today's Focus ([DATE])

### ⚡ Top Priority (2-3 hours)
[Single most important task today]
- **Task**: [Description]
- **Why now**: [Urgency/blocking reason]
- **Blocks**: [What depends on this]
- **Context**: [Relevant background from recent work]
- **Success criteria**: [How to know it's done]

### 📌 Secondary Tasks (1-2 hours each)
[2-3 important but not urgent tasks]
- **Task 1**: [Description]
  → Est: X hours | Impact: High/Medium

- **Task 2**: [Description]
  → Est: X hours | Impact: High/Medium

### 🎯 Stretch Goals (if time permits)
[1-2 nice-to-have tasks for extra time]
- [Task that can be done if ahead of schedule]
- [Quick win or preparation for tomorrow]

### ⏰ Time Budget Check
- Top Priority: 2-3 hours
- Secondary Tasks: 2-4 hours
- Stretch Goals: 1-2 hours
- **Total: 5-9 hours**

### 💡 Focus Recommendation
[Specific advice on how to approach today's work]
- Recommended order: [Task sequence]
- Deep work needed: [Which tasks need focus]
- Quick wins: [Tasks that can be done quickly]
- Blockers to resolve: [What's in the way]

### 🚫 Not Today
[Tasks that are important but should wait]
- [Task]: Wait until [dependency] is resolved
- [Task]: Schedule for [later time]

---

## Selection Criteria

When selecting tasks, prioritize based on:
1. **Blockers**: Tasks that are blocking other work
2. **Urgency**: Deadlines or time-sensitive items
3. **Dependencies**: Prerequisites for planned work
4. **Energy level**: Match task difficulty to typical daily energy curve
5. **Momentum**: Build on recent progress

## Time Management

Support optional arguments:
- `--hours N` : Plan for N hours of work (default: 6-8)
- `--energy high|normal|low` : Adjust for energy level
- `--mode deep|varied|quick` : Focus style preference

Examples:
```bash
/research-memory:focus
/research-memory:focus --hours 4
/research-memory:focus --energy low --mode quick
```

## Focus Tips

Include practical advice:
- **Deep work blocks**: Suggest 90-120 min focused sessions
- **Break strategy**: Recommend when to take breaks
- **Context switching**: Minimize by grouping similar tasks
- **Energy management**: Hard tasks when fresh, routine tasks when tired

## Integration with Other Commands

Suggest complementary commands:
- "Run `/research-memory:status` to see current state"
- "Use `/research-memory:remember` at end of day to log progress"
- "Check `/research-memory:insights` if feeling stuck"

Be specific, actionable, and realistic. Help the user make actual progress today, not just plan theoretically.
