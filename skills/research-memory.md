---
name: research-memory
description: Academic research memory management skill for tracking project continuity, decisions, and experiments across sessions
---

# Research Memory Skill

An academic research project memory management skill that helps maintain context across different sessions, enabling researchers to quickly resume work and track progress through complex research workflows.

## Overview

The `research-memory` skill provides three core capabilities for academic research projects:

1. **Context Bootstrap** - Quickly restore project state and recent progress
2. **Session Logging** - Document research activities with structured phase segmentation
3. **Historical Query** - Search past decisions, experiments, and insights

## When to Use

### Starting a Research Session
Trigger when you want to resume work on a project:
- "我上次做到哪儿了？"
- "帮我恢复一下项目状态"
- "用 research-memory 总结一下最近的进展"
- "今天应该做什么？"

### Documenting Progress
Trigger when you want to record research activities:
- "帮我记录今天的工作"
- "记一条 research log"
- "把这个实验结果记到 research-memory 里"
- "用 research-memory 总结这个 session"

### Querying History
Trigger when you need to find past information:
- "我们之前为什么放弃过这个方案？"
- "H2 相关的实验有哪些？"
- "关于数据处理的决定有哪些记录？"
- "查一下之前关于变量构造的讨论"

## Tools

### research_memory_bootstrap

**Purpose**: Restore project context and generate work plan suggestions

**Behavior**:
- Reads `memory/project-overview.md` for project context
- Extracts recent N entries from `memory/devlog.md` (configurable, default: 5)
- Gathers open TODOs from `memory/todos.md`
- Generates structured summary and suggested work plan

**Example Usage**:
```
User: "帮我用 research-memory 恢复一下上次做到哪一步，并给一个今天的 plan。"
Claude: [Calls research_memory_bootstrap]
Returns: Recent progress summary + Current TODOs + Suggested work plan
```

### research_memory_log_session

**Purpose**: Document research session with structured phase segmentation

**Input Structure**:
```python
{
    "session_goal": "Main objective of this session",
    "changes_summary": "Summary of changes made",
    "experiments": [
        {
            "hypothesis": "H1: X affects Y",
            "dataset": "sample_data_v2",
            "model": "OLS regression",
            "metrics": {"r_squared": 0.75, "p_value": 0.02},
            "notes": "Unexpected heteroscedasticity observed"
        }
    ],
    "decisions": [
        {
            "decision": "Switched from linear to log transformation",
            "rationale": "Better normality of residuals",
            "alternatives_considered": ["Box-Cox transformation", "Non-parametric methods"]
        }
    ],
    "todos": ["Test robustness with alternative specifications", "Add control variables"],
    "phases": {
        "data_preprocess": "Applied log transformation to dependent variable",
        "modeling": "Estimated OLS with robust standard errors",
        "robustness": "Tested with alternative functional forms",
        "notes": "Consider interaction terms for next iteration"
    }
}
```

**Behavior**:
- Appends timestamped entry to `memory/devlog.md` with phase segmentation
- Updates `memory/experiments.csv` with structured experiment records
- Records significant decisions in `memory/decisions.md`
- Updates `memory/todos.md` with new items and completion status
- Updates `memory/project-overview.md` for new long-term information

**Example Usage**:
```
User: "这一段工作帮我整理成一条 research-memory 记录。"
Claude: [Analyzes conversation, extracts structured information, calls research_memory_log_session]
```

### research_memory_query_history

**Purpose**: Search and retrieve relevant historical information

**Behavior**:
- Performs keyword search across `memory/devlog.md`, `memory/decisions.md`, and `memory/experiments.csv`
- Filters results by research phase, date range, or content type if specified
- Provides concise summary with relevant excerpts
- Includes timestamps and context for each match

**Example Usage**:
```
User: "我们之前为什么放弃过空间 lag 模型？"
Claude: [Calls research_memory_query_history with query about spatial lag models]
Returns: Summary of decision rationale + Relevant excerpts from decisions.md and devlog.md
```

## Research Phases Supported

The skill recognizes and organizes content by these academic research phases:

- **DGP**: Data Generating Process documentation and assumptions
- **data_preprocess**: Data cleaning, variable construction, missing value handling
- **data_analyse**: Descriptive statistics, visualization, correlation analysis
- **modeling**: Model specification, estimation methods, hyperparameter tuning
- **robustness**: Sensitivity analysis, alternative specifications, validation tests
- **writing**: Documentation, paper writing, figure preparation
- **infra**: Environment setup, code organization, tooling changes
- **notes**: General observations, intuitions, future ideas

## Memory File Structure

The skill creates and manages these files in the `memory/` directory:

- `project-overview.md` - Long-term project knowledge (research questions, hypotheses, datasets)
- `devlog.md` - Time-ordered development and experiment logs
- `decisions.md` - Key decisions with rationale and alternatives considered
- `experiments.csv` - Structured experiment records with metrics and metadata
- `todos.md` - TODO items and open questions with checkbox tracking

## Usage Examples

### Example 1: Daily Session Start
```
User: "早上好！帮我用 research-memory 恢复一下项目状态。"

Claude: [Calls research_memory_bootstrap]

**项目状态恢复 (2025-12-02)**

**最近进展摘要:**
- 11月30日：完成数据清洗和异常值处理
- 12月1日：建立基础回归模型，R²=0.72
- 12月1日：发现异方差问题，改用稳健标准误

**当前待办事项:**
- [ ] 检验多重共线性问题
- [ ] 添加控制变量（教育水平、工作经验）
- [ ] 进行稳健性检验（替换变量构造方式）

**建议今日工作计划:**
1. 解决异方差问题的根本原因（考虑变量变换）
2. 添加更多控制变量提高模型解释力
3. 开始准备初步结果表格用于论文写作
```

### Example 2: Session Documentation
```
User: "今天的工作帮我记到 research-memory 里，主要解决了异方差问题。"

Claude: [Analyzes session, extracts structured information, calls research_memory_log_session]

✅ 已记录到 research-memory：

**会话目标**: 解决回归模型中的异方差问题

**主要进展**:
- data_preprocess: 对因变量进行对数变换，显著改善残差分布
- modeling: 使用对数线性模型，R²提升至0.78
- robustness: 通过Breusch-Pagan检验确认异方差问题已解决

**实验记录**:
- 模型: 对数线性回归 (log(Y) = β₀ + β₁X + ε)
- 数据集: sample_data_v2_cleaned
- 指标: R²=0.78, F-statistic=45.3, p<0.001
- 诊断: Breusch-Pagan检验 p=0.15（无法拒绝同方差假设）

**关键决定**:
- 决定：采用对数变换而非加权最小二乘法
- 原因：对数变换同时改善了线性性和异方差问题
- 备选方案：考虑过Box-Cox变换，但对数变换解释性更强

**更新待办事项**:
- [x] 解决异方差问题
- [ ] 进行VIF检验检查多重共线性
- [ ] 添加更多控制变量
- [ ] 准备结果可视化
```

### Example 3: Historical Query
```
User: "查一下我们之前关于变量构造的所有讨论。"

Claude: [Calls research_memory_query_history]

**变量构造相关记录**:

**2025-11-28 - devlog.md:**
> **data_preprocess**: 对收入变量进行winsorize处理（1%和99%分位数）
> 原因：发现极端异常值影响回归结果，最大值超过均值100倍
> 方法：使用scipy.stats.mstats.winsorize，两端各截断1%

**2025-11-29 - decisions.md:**
> **决定**: 添加年龄的二次项作为控制变量
> **理由**: 观察到年龄与因变量存在非线性关系（U型曲线）
> **验证**: 残差图显示加入二次项后模式明显改善

**2025-12-01 - experiments.csv:**
> experiment_id: exp_2025_001, hypothesis: "H1: 教育回报非线性",
> variables: "age, age_squared, log_income, experience",
> result: "age_squared系数显著为正（p<0.01），支持非线性假设"

**总结**:
- 处理了收入变量的极端异常值（winsorize）
- 添加了年龄的二次项以捕捉非线性效应
- 对数变换改善了收入变量的分布
- 所有变换都经过了统计检验和可视化验证
```

## Configuration

The skill supports configuration through `config/config.json`:

```json
{
    "bootstrap": {
        "recent_entries_count": 5,
        "include_todos": true,
        "suggest_work_plan": true
    },
    "logging": {
        "auto_timestamp": true,
        "phase_sections": ["DGP", "data_preprocess", "data_analyse", "modeling", "robustness", "writing", "infra", "notes"],
        "experiment_schema": ["hypothesis", "dataset", "model", "metrics", "notes"]
    },
    "search": {
        "max_results": 10,
        "include_context": true,
        "context_lines": 3
    }
}
```

## Future Extensibility

This v0 implementation uses local files but provides clear migration paths to v1:

- **Backend Abstraction**: All storage operations go through `MemoryBackend` interface
- **Schema Evolution**: JSON-based schemas support versioning and validation
- **Search Enhancement**: File-based search can be replaced with vector search
- **Collaboration**: Individual memory files can be merged to shared databases

## Best Practices

1. **Consistent Logging**: Log sessions regularly, preferably at major milestones
2. **Structured Queries**: Be specific about research phases when querying history
3. **Decision Documentation**: Always include rationale and alternatives for key decisions
4. **Regular Bootstrap**: Use bootstrap functionality at the start of each work session
5. **TODO Maintenance**: Keep todos current and mark completed items

This skill helps maintain research continuity and accelerates academic progress by preserving institutional knowledge and decision rationale across the research lifecycle.