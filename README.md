## 🌐 Language / 言語 / 语言

[**English**](README.md) | [日本語](README.ja.md) | [简体中文](README.zh.md) 

---

A Claude Code skill designed for academic research projects to manage and record project-level long-term memory, helping researchers maintain context continuity between different sessions.

## Project Overview

This skill addresses a core problem in academic research: how to effectively record and manage knowledge, decisions, and experimental trajectories throughout the research process, enabling quick context restoration after project interruptions and avoiding repetitive work.

## 🚀 Quick Start

### 1. Requirements

- **Python**: 3.8 or higher
- **Claude Code**: Latest version
- No additional dependencies required (uses Python standard library)

### 2. Installation in Existing Projects

Integrate the research-memory skill into your academic research project:

```bash
# 1. Clone or download this repository
git clone https://github.com/syfyufei/research-memory.git
cd research-memory

# 2. Copy core files to your project
cp SKILL.md /path/to/your/project/
cp handlers.py /path/to/your/project/
cp -r config/ /path/to/your/project/
cp -r .claude/ /path/to/your/project/

# 3. Create memory directory (optional, will be created automatically on first use)
mkdir -p /path/to/your/project/memory
```

### 3. Verify Installation

Test in your project directory:

```bash
# Test basic functionality
python3 handlers.py bootstrap

# Test search functionality
python3 handlers.py query --question "test"
```

### 4. Start Using

In Claude Code, you can trigger research-memory functionality through natural language:

```
User: "Good morning! Help me restore the project status using research-memory."
Claude: [Automatically analyzes project and restores context]
```

## 🔧 Configuration Options

Customize skill behavior through `config/config.json`:

```json
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
  "search": {
    "max_results": 10,
    "include_context": true,
    "context_lines": 3
  }
}
```

### Configuration Description

- `memory_directory`: Memory file storage directory (default: "memory")
- `encoding`: File encoding format (default: "utf-8")
- `timestamp_format`: Timestamp format ("ISO8601", "YYYY-MM-DD_HH-MM-SS", "timestamp")
- `bootstrap.recent_entries_count`: Number of recent entries to show during recovery
- `search.max_results`: Maximum number of search results to return

## 🎯 Core Features

### 1. Research Context Recovery (`research_memory_bootstrap`)
Quickly restore project status, including:
- Recent research progress summary
- Current TODO items
- Work suggestions based on historical records

**Usage Examples**:
```
"Help me use research-memory to restore where I left off"
"What's today's research plan?"
"What's the current project status and next steps?"
```

### 2. Research Session Logging (`research_memory_log_session`)
Structured recording of research activities, supporting:
- Research phase-grouped records (DGP, data preprocessing, modeling, etc.)
- Systematic storage of experimental results
- Decision reasoning and alternative options recording
- **New TODO status tracking** (pending/completed/cancelled)
- Priority and category management

**Usage Examples**:
```
"Record today's work in research-memory"
"Log the results of that experiment I just ran"
"Help me summarize this session and update TODOs"
"Mark data processing tasks as completed, add new modeling tasks"
```

### 3. Historical Record Query (`research_memory_query_history`)
Efficient retrieval of historical information:
- Keyword search (supports Chinese and English)
- Filter by research phase
- Cross-file comprehensive search
- **Advanced filtering options** (date range, content type, result count limit)

**Usage Examples**:
```
"Why did we abandon the spatial lag model before?"
"What experiments are related to H2?"
"Discussion records about variable construction"
"Query all modeling records from the past week"
"Find entries about digital skills in experiment records"
```

## Supported Research Phases

- **DGP**: Data generating process documentation and hypotheses
- **data_preprocess**: Data cleaning, variable construction, missing value handling
- **data_analyse**: Descriptive statistics, visualization, correlation analysis
- **modeling**: Model specification, estimation methods, hyperparameter tuning
- **robustness**: Robustness checks, alternative specifications, validation tests
- **writing**: Documentation, paper writing, figure preparation
- **infra**: Environment configuration, code organization, tool changes
- **notes**: General observations, intuitive ideas, future ideas

## 📁 Project Structure

Directory structure after integration into your project:

```
your-research-project/
├── SKILL.md                          # Research Memory skill definition
├── handlers.py                       # Core implementation logic
├── config/
│   └── config.json                   # Configuration file
├── .claude/
│   └── CLAUDE.md                     # Claude Code project description
├── memory/                           # Research memory storage
│   ├── project-overview.md           # Long-term project knowledge
│   ├── devlog.md                     # Time-ordered development log
│   ├── decisions.md                  # Key decisions and reasons
│   ├── experiments.csv               # Structured experiment records
│   └── todos.md                      # TODO item management
└── ...                              # Your other project files
```

## 💻 Advanced CLI Usage

In addition to using through Claude Code, you can directly access more powerful features via command line:

```bash
# Basic query
python3 handlers.py query --question "digital skills"

# Advanced filtering queries
python3 handlers.py query --question "modeling" --limit 5
python3 handlers.py query --question "data" --type experiments
python3 handlers.py query --question "decision" --from-date 2025-12-01 --to-date 2025-12-03
python3 handlers.py query --question "analysis" --phase modeling

# Complete session recording (supports new TODO format)
python3 handlers.py log-session --payload-json '{
  "session_goal": "Complete data modeling analysis",
  "todos": [
    {
      "text": "Data cleaning and preprocessing",
      "status": "completed",
      "completion_note": "Completed missing value handling and outlier detection"
    },
    {
      "text": "Build linear regression model",
      "status": "pending",
      "priority": "high",
      "category": "modeling"
    }
  ],
  "phases": {
    "data_preprocess": "Use winsorize for outlier handling",
    "modeling": "Estimate basic regression model",
    "notes": "Found model R²=0.72, heteroskedasticity issue exists"
  }
}'
```

### CLI Filtering Options Description

- `--question`: Search query keywords (required)
- `--limit`: Limit result count
- `--type`: Filter by content type (devlog/decisions/experiments)
- `--from-date`: Start date (YYYY-MM-DD format)
- `--to-date`: End date (YYYY-MM-DD format)
- `--phase`: Filter by research phase (DGP/data_preprocess/modeling, etc.)

## 🚀 New Feature Highlights (v0.2)

### ✅ Complete Configuration
- **All config fields functional**: `memory_directory`, `encoding`, `csv_delimiter`, etc.
- **Deep configuration merge**: Support user custom override of default configurations
- **Multi-encoding support**: Perfect support for Chinese encoding (UTF-8, GBK, etc.)

### ✅ Smart TODO Management
- **Unified status tracking**: pending/completed/cancelled three states
- **Priority management**: high/medium/low priority marking
- **Category system**: Support custom categories (analysis/modeling/writing, etc.)
- **Auto-completion marking**: Intelligently identify and mark completed TODOs

### ✅ Advanced Search Filtering
- **Multi-dimensional filtering**: Filter by date range, content type, research phase
- **Result count control**: Flexibly limit search result count
- **CLI enhancement**: Complete command-line filtering options

### ✅ Data Integrity Guarantee
- **Experiment ID collision prevention**: Millisecond timestamp + UUID suffix
- **File format fixes**: Perfect handling of separators and newlines
- **Incremental updates**: Intelligently protect existing content, avoid duplication

## Technical Features

### v0 Core Features
- **Local file storage**: No database needed, uses Markdown + CSV
- **Incremental updates**: Protect existing content, avoid duplicate recording
- **Multilingual support**: Full support for Chinese-English mixed recording
- **Academic orientation**: Optimized for academic research workflow

### v1 Planned Extensions
- **Database backend**: Upgradable to SQLite/PostgreSQL
- **Vector search**: Support semantic search
- **MCP integration**: Support remote memory access
- **Collaboration features**: Multi-user memory sharing

## 🎯 Use Cases

### Individual Researchers
- Quick context restoration after long project interruptions
- Avoid repetitive work and decision forgetting
- Systematic recording of experiments and results

### Research Teams
- Knowledge transfer and decision tracing
- Avoid repetitive errors
- Maintain team research memory

### Academic Writing
- Structured recording of methodology sections
- Systematic management of experimental results
- Complete tracing of decision-making processes

## 🔄 Recommended Workflow

### Daily Research Start
```
User: "Good morning! Help me use research-memory to restore project status and give me a plan for today."
Claude: [Auto-call bootstrap → Provide recent progress + TODOs + work suggestions]
```

### Research Process Recording
```
User: "These experimental results are good, help me record them."
Claude: [Auto-extract information → Structured recording → Update experiments and TODOs]
```

### Historical Decision Query
```
User: "Why did we choose linear model instead of nonlinear model before?"
Claude: [Auto-search → Provide decision reasoning + alternatives + related experiment records]
```

### Progress Summary
```
User: "Help me use research-memory to summarize today's work and update TODOs."
Claude: [Auto-summarize → Mark completed items → Add new TODOs]
```

## 🏆 Development Status

### ✅ v0.2 Completed Features
- **Complete configuration**: All config fields functional, multi-encoding support
- **Smart TODO management**: Unified status tracking, priority and category management
- **Advanced search filtering**: Multi-dimensional filtering, CLI enhanced options
- **Data integrity guarantee**: Experiment ID collision prevention, file format fixes
- **Backward compatibility**: Maintains compatibility with old format payloads

### 📋 Roadmap
- **v0.3**: [Planning] Experiment validation and schema enforcement
- **v0.4**: [Planning] Performance optimization and large file support
- **v1.0**: [Long-term goal] Database backend + vector search

## 🤝 Contributing Guidelines

Contributions welcome! This project follows standard academic software development practices:

1. **Code Quality**: Maintain clear comments and documentation
2. **Test Coverage**: Ensure functionality correctness and stability
3. **User Friendly**: Provide clear usage instructions and examples
4. **Backward Compatibility**: Smooth migration path from v0 to v1

### Contribution Process
1. Fork the project
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

## 📄 License

MIT License - Free to use and modify

## 📞 Contact

- **Author**: Yufei Sun (Adrian) <syfyufei@gmail.com>
- **Project URL**: https://github.com/syfyufei/research-memory
- **Issue Reporting**: [GitHub Issues](https://github.com/syfyufei/research-memory/issues)

## 🙏 Acknowledgments

Thanks to all developers and researchers who contribute to the development of academic research tools. This skill aims to help researchers better manage research memory and improve the efficiency and quality of academic research.

---

**Let research memory no longer be lost, let knowledge accumulation be more valuable!** 🧠✨

---

This skill aims to help researchers better manage and utilize knowledge accumulation during the research process, improving the efficiency and quality of academic research.