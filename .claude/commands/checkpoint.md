---
description: Create a named checkpoint of current state
---

Use the research-memory skill to create a checkpoint of the current project state.

Ask the user for a checkpoint name/description if not provided.

A checkpoint captures:
- Current timestamp
- Checkpoint name/tag
- Project state summary
- Recent work summary
- Active TODOs at this point
- Key metrics snapshot

Log the checkpoint to `memory/checkpoints.md` in this format:

```markdown
## Checkpoint: [NAME] (YYYY-MM-DD HH:MM)

**Purpose**: [User's description]

**Project State**:
- Phase: [Current phase]
- Progress: [Brief summary]
- Open TODOs: X items
- Recent experiments: Y

**Key Metrics**:
- Total sessions: N
- Experiments run: M
- Decisions made: P

**Notable Context**:
- [Important note 1]
- [Important note 2]

---
```

After creating the checkpoint, confirm:
- Where it was saved
- How to reference it later
- Suggest using it as a comparison point

Use cases:
- Before major changes: `/research-memory:checkpoint "Before refactor"`
- Milestones: `/research-memory:checkpoint "Paper draft v1 complete"`
- Experiments: `/research-memory:checkpoint "Baseline model finalized"`
- Reviews: `/research-memory:checkpoint "End of sprint 3"`

Support optional arguments:
- `--tag milestone` : Mark as a milestone checkpoint
- `--tag experiment` : Mark as an experiment checkpoint
- `--tag backup` : Mark as a safety backup point
