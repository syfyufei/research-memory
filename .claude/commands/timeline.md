---
description: Visualize project timeline
---

Use the research-memory skill to create a visual project timeline.

Read `memory/devlog.md`, `memory/experiments.csv`, and `memory/decisions.md` to extract:
- All dated entries
- Experiments with timestamps
- Decision points

Present as a chronological timeline:

```
2025-11-15 | [DATA] Data cleaning completed - removed 150 outliers
2025-11-18 | [MODEL] Baseline model R²=0.72
2025-11-20 | [DECISION] Chose log transformation over Box-Cox
2025-11-22 | [ROBUST] Heteroscedasticity test passed
2025-11-25 | [EXPERIMENT] Added control variables, R²→0.78
2025-12-01 | [WRITING] Started draft of results section
```

Use emoji indicators for different activities:
- 📊 Data processing
- 🔬 Experiments
- 🤔 Decisions
- ✅ Completed milestones
- 📝 Writing

Support optional arguments:
- `--last 7d` : Show last 7 days
- `--last 30d` : Show last 30 days
- `--from YYYY-MM-DD --to YYYY-MM-DD` : Custom date range

If no arguments provided, show last 14 days by default.
