[**English**](README.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="https://maas-log-prod.cn-wlcb.ufileos.com/anthropic/c40838a3-d7bd-48b7-aa5c-ffc7e375eafa/361cbdc75b756c1a65f45153a2b60a0a.png?UCloudPublicKey=TOKEN_e15ba47a-d098-4fbd-9afc-a0dcf0e4e621&Expires=1764755166&Signature=j3dFWqiM%2BLqbBUWEMIR5C0jipSk%3D" alt="Research Memory Banner" width="100%"/>
</p>

We all know how academic research really works:

1. **Your research cycles will inevitably stretch far beyond your initial timeline.**
2. **You'll inevitably have more repositories open simultaneously than you intended.**
3. **When you return to a project, you'll inevitably have forgotten where you left off.**

If you're a developer who works with AI assistants, this scenario probably feels all too familiar:

> You open a repository that's been sitting untouched for three months,
> Scroll through `git log` from top to bottom,
> All your notebooks, scripts, and paper drafts are still there,
> But only one question echoes in your mind:
> **"Where exactly did I leave things last time?"**

Here's what makes it even more frustrating:
**You've forgotten, and so has your LLM assistant.**
Starting a fresh conversation, the LLM only has access to "the current few screens of context",
yet has absolutely no understanding of all the struggles, detours, and breakthroughs you've navigated through over the past few months.

`research-memory` is designed to create a **truly "long-term" project-level memory layer** during your development process:

- It doesn't try to be a general-purpose RAG system or help you memorize literature;
- It faithfully records what you and your AI assistant accomplish in this project:
  **what you did, how you did it, why you chose that approach, and what comes next**.

In other words:

> Empower "future you + your current AI assistant"
> to seamlessly continue where "past you" left off,
> rather than starting from scratch with a blank conversation every single time.


## Quick Overview (TL;DR)

`research-memory` is a Claude Code Skill / Python tool specifically designed for academic research projects, providing three essential capabilities:

1. **Session Bootstrap: `research_memory_bootstrap`**
   - Pulls from your `memory/` directory:
     - Project overview (research questions, hypotheses, data sources...)
     - Recent N devlog entries
     - Current TODO list
   - Automatically generates "recent progress + suggested work plan"

2. **Session Logging: `research_memory_log_session`**
   - Structured recording of research work into:
     - `devlog.md`: Organized by research phases (DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes)
     - `experiments.csv`: One line per experiment (hypothesis/dataset/model/metrics/notes...)
     - `decisions.md`: Key decisions and their rationale/alternatives
     - `todos.md`: Add new items while marking completed ones as `[x]`

3. **History Query: `research_memory_query_history`**
   - Search using keywords + simple filters (date / phase / type) across:
     - `devlog.md`
     - `decisions.md`
     - `experiments.csv`
   - Returns summaries + key snippets.

**Everything runs on local text files (Markdown + CSV), plays nicely with Git, is manually editable, and has zero external service dependencies.**

---

## Architecture Overview

Overall structure:

```text
research-memory/
├── handlers.py        # Skill's Python implementation & CLI entry point
├── SKILL.md           # Claude Code Skill description (tool definitions)
├── config/
│   └── config.json    # Skill behavior configuration
├── .claude/
│   ├── CLAUDE.md      # Project-level instructions, telling Claude when to use this skill
│   └── settings.local.json  # Claude Code local settings example
└── memory/            # Actual "project memory layer" (auto-creatable)
    ├── project-overview.md  # Long-term project information
    ├── devlog.md            # Development/analysis log (by session + phase)
    ├── decisions.md         # Key decision records
    ├── experiments.csv      # Experiment table (structured)
    └── todos.md             # TODO / open questions
```

Core components:

* **Skill Layer**

  * `SKILL.md` defines three tools:

    * `research_memory_bootstrap`
    * `research_memory_log_session`
    * `research_memory_query_history`
  * Called by Claude Code to corresponding functions in `handlers.py`.

* **Backend Layer**

  * `MemoryBackend` encapsulates all file I/O, configuration loading, and TODO processing logic:

    * Currently local Markdown + CSV;
    * Can be replaced with SQLite / vector database / MCP server in the future without changing the outer interface.

---

## Installation

In Claude Code, register the marketplace first:

```bash
/plugin marketplace add syfyufei/research-memory
```

Then install the plugin from this marketplace:

```bash
/plugin install research-memory@research-memory-marketplace
```

### Verify Installation

Test the skill by using it in Claude Code:

```
"Research Memory, help me get back up to speed with my project"
```

If the skill is installed correctly, Claude will use the research-memory tools to bootstrap your project context. Research Memory will automatically create the necessary `memory/` directory and files on first use.

### Quick Start

Simply use natural language in Claude Code:

```
"Research Memory, help me get back up to speed with my project"
"Log this work session to Research Memory"
"Search for our decisions about spatial lag models"
```

### Uninstallation

**If installed via marketplace**:

```bash
claude plugin uninstall research-memory
```

**If installed manually**:

```bash
# Remove the skill files from your project
rm -f handlers.py config/config.json .claude/CLAUDE.md SKILL.md
rm -rf config/ .claude/ memory/
```

---

## Configuration: `config/config.json`

All behavior is controlled by one JSON configuration file, default configuration looks like this (excerpt):

```jsonc
{
  "memory_directory": "memory",
  "encoding": "utf-8",
  "csv_delimiter": ",",
  "timestamp_format": "ISO8601",

  "bootstrap": {
    "recent_entries_count": 5,
    "include_todos": true,
    "suggest_work_plan": true
  },

  "logging": {
    "auto_timestamp": true,
    "phase_sections": [
      "DGP",
      "data_preprocess",
      "data_analyse",
      "modeling",
      "robustness",
      "writing",
      "infra",
      "notes"
    ],
    "experiment_schema": [
      "hypothesis",
      "dataset",
      "model",
      "metrics",
      "notes"
    ]
  },

  "search": {
    "max_results": 10,
    "include_context": true,
    "context_lines": 3
  }
}
```

Key field descriptions:

* `memory_directory`: Memory file directory (relative to project root);

* `encoding`: File encoding (default `utf-8`, can also be changed to `gbk`, etc.);

* `timestamp_format`:

  * `"ISO8601"` → e.g., `2025-12-03T19:30:00+09:00`
  * `"YYYY-MM-DD_HH-MM-SS"` → suitable for filenames / human reading
  * `"timestamp"` → Unix timestamp (seconds);

* `bootstrap.recent_entries_count`: How many recent devlog entries to show on startup;

* `logging.phase_sections`: Supported research phase tags;

* `logging.experiment_schema`: Required fields in `experiments.csv`;

* `search.*`: Number of results returned on query and whether to include context.

You can modify `config.json` as needed, all configuration items are effective in `MemoryBackend`.

---

## Using with Claude Code

### Typical Usage Patterns

**1. Starting your day: Getting back up to speed**

> "Hey, help me get back up to speed with my research using research-memory, and suggest a plan for today."

Here's what happens:

* Calls `research_memory_bootstrap`:

  * Reads `project-overview.md` (if it exists);
  * Extracts recent N devlog entries (with timestamps + phase info);
  * Summarizes current incomplete TODOs;
  * Generates a "today's work suggestion plan".

---

**2. Completing a work session: Logging your progress**

> "Help me organize this work session into a research log, broken down by DGP / data_analyse / modeling phases, and save it to research-memory."

Claude will:

1. Based on current conversation content and what you just did, construct a payload, for example:

   ```jsonc
   {
     "session_goal": "Run spatial DiD on MCIB_v1.3 to verify H2",
     "changes_summary": [
       "Updated 01_clean_mcib.R, added treat_window_180 variable",
       "Filtered municipalities with sample count < 100"
     ],
     "phases": {
       "DGP": "Assume treatment effects gradually appear within 0-180 days, use distance threshold 50km to construct weight matrix.",
       "data_analyse": "Plot baseline period cognitive mean comparison for treatment/control groups, no obvious pre-trend crossover observed.",
       "modeling": "Estimate two specifications: TWFE + cluster by municipality; extended specification with provincial time trends.",
       "robustness": "Simple placebo: shift treatment time by 1 year overall, results not significant."
     },
     "experiments": [
       {
         "hypothesis": "H2",
         "dataset": "MCIB_v1.3",
         "model": "Spatial DiD with 50km binary contiguity W",
         "metrics": {
           "ATT": 0.153,
           "p_value": 0.021
         },
         "notes": "Results sensitive to window setting, need further robustness checks."
       }
     ],
     "decisions": [
       {
         "title": "Tentatively adopt Model B as main specification",
         "rationale": "Pre-trend smoother after adding provincial time trends, coefficients more stable.",
         "alternatives": [
           "Continue using simple TWFE as main specification",
           "Try event-study form"
         ]
       }
     ],
     "todos": [
       "Add k-nearest neighbors based spatial weight matrix comparison",
       "Systematically organize placebo/alternative spec results into paper.qmd"
     ],
     "completed_todos": [
       "Add spatial weight matrix construction explanation in Methods section"
     ]
   }
   ```

2. Call `research_memory_log_session(payload)`, automatically:

   * Append a timestamped session record to `devlog.md`;
   * Insert a complete experiment information row to `experiments.csv`;
   * Write decision block to `decisions.md`;
   * Add new TODOs to `todos.md`, and mark items in `completed_todos` as completed.

After that, you just need to naturally describe "what you just did", and the Skill will help you turn it into structured memory that can be long-term retrieved.

---

**3. Looking back: Reviewing past decisions and experiments**

> "Why did we abandon spatial lag models before?"
> "Show me all experiments we ran for H2."
> "Look up changes related to hksarg_parser.R."

Claude will call:

```python
query_history(query, filters=None)
```

The Skill will:

* Perform keyword matching across `devlog.md` / `decisions.md` / `experiments.csv`;
* Return up to `search.max_results` matches per your configuration;
* Attach necessary context (a few lines before and after);
* Generate a brief summary, telling you:

  * What decisions were made at that time;
  * Which experiments were conducted;
  * Which alternative approaches/specifications were abandoned.

---

## Command Line Usage (Optional)

Besides calling through Claude Code, you can also directly operate `handlers.py` from the command line—suitable for when you temporarily don't have Claude open, or want to use scripts for batch processing.

### 1. Bootstrap

```bash
python handlers.py bootstrap
```

Output a JSON, including:

* `project_context`
* `recent_progress`
* `current_todos`
* `work_plan_suggestions`
* `timestamp`

### 2. Record Session

```bash
python handlers.py log-session \
  --payload-json '{
    "session_goal": "Test CLI logging",
    "changes_summary": ["Update README examples"],
    "phases": {"notes": "First time using research-memory from command line"},
    "todos": ["Reference this tool in paper.qmd"]
  }'
```

### 3. Query History

```bash
# Simplest: search by keywords
python handlers.py query --question "spatial lag model"

# With filters: time + phase + type
python handlers.py query \
  --question "H2" \
  --from-date 2025-01-01 \
  --to-date 2025-12-31 \
  --phase modeling \
  --type experiments \
  --limit 5
```

CLI will output JSON, convenient for you to continue using in other scripts.

---

## File Format Examples

### `memory/devlog.md`

```markdown
# Development Log

## 2025-12-03 10:15

**Session Goal**: Run spatial DiD on MCIB_v1.3 to verify H2

**Changes Summary**:
- Updated 01_clean_mcib.R, added treat_window_180 variable
- Filtered out municipalities with sample count < 100

### DGP
Assume treatment effects gradually appear within 0-180 days, use 50km threshold to construct binary spatial weight matrix and row standardize.

### data_analyse
Plot baseline period cognitive mean comparison for treatment vs control groups, no obvious pre-trend crossover observed.

### modeling
Estimate two specifications: Model A (TWFE), Model B (TWFE + provincial time trends), H2 coefficients consistent in both directions.

### robustness
Did simple placebo test (shift treatment time by one year overall), effect not significant.

### notes
Need to further try event-study and different spatial weight matrices.

---

```

### `memory/experiments.csv` (header example)

```csv
timestamp,experiment_id,hypothesis,dataset,model,metrics,notes,research_phase
2025-12-03T10:15:00+09:00,exp_20251203_101500,H2,MCIB_v1.3,"Spatial DiD, W=50km",{"ATT":0.153,"p_value":0.021},"placebo results unstable","DGP,data_analyse,modeling,robustness"
```

### `memory/todos.md`

```markdown
# Project TODOs

- [ ] Add k-nearest neighbors based spatial weight matrix comparison
- [x] Add spatial weight matrix construction explanation in Methods section (completed: 2025-12-03 - via log_session)
```

### `memory/decisions.md`

```markdown
# Key Decisions

## 2025-12-03 10:20 — Tentatively adopt Model B as main specification

**Decision**
Use TWFE with provincial time trends as main specification.

**Rationale**
Pre-trend smoother, estimation results more stable across different subsamples.

**Alternatives**
- Keep simple TWFE as main specification
- Switch to event-study + group-specific trends
```

---

## Design Principles

* **Local-first**: Everything is local text files, Git-manageable, manually editable;
* **Skill-first**: Claude Code calls through skill tools, you don't need to care about specific file paths;
* **Extensible**: Through `MemoryBackend` abstraction layer, can seamlessly switch to database / MCP / remote services in the future;
* **Semantically aligned with research workflow**:

  * DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes
  * Instead of just writing a few lines like "changed some code today".

---

## Roadmap

Current version is **v0.x (file backend version)**, future considerations include:

* Support SQLite / DuckDB as backend (stronger query capabilities, support aggregation analysis);
* Add vector retrieval, provide fuzzy matching for long devlogs;
* MCP / HTTP service mode, can be shared by multiple projects / Agents;
* Locking and merge strategies for multi-user collaboration scenarios.

---

## License & Author

* **License**: MIT
* **Author**: Yufei Sun (Adrian) `<syfyufei@gmail.com>`
* **Repo**: [https://github.com/syfyufei/research-memory](https://github.com/syfyufei/research-memory)

---

If you frequently juggle multiple large projects
and dread spending half a day each time "remembering what yesterday's you was thinking",
try installing `research-memory` into your research repositories—
let Claude Code become a partner that **truly remembers your entire project history**,
instead of just a chat interface that only remembers the current conversation.

```
::contentReference[oaicite:0]{index=0}
```