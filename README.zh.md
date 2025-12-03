[**English**](README.md) | [日本語](README.ja.md) | [简体中文](README.zh.md) 

学术项目往往：

1. **研究周期一定会比你想的长。**  
2. **同时开的 repo 一定会比你想的多。**  
3. **等你下次回来的时候，一定会忘了自己在干嘛。**

在 vibe-coding 的日常里，这大概是最常见的一幕：

> 打开一个放了三个月的 repo，  
> `git log` 从上翻到下，  
> notebook、脚本、paper draft 全都在，  
> 但脑子里只有一个问题：  
> **「我上次做到哪一步了？」**

更尴尬的是：  
**你忘了，LLM 也忘了。**  
新开一个对话，LLM 只知道“当前这几屏上下文”，  
却完全不了解你这个项目过去几个月的所有折腾、绕路和顿悟。

`research-memory` 想做的，就是在 vibe-coding 的过程中，  
给每个项目加一层**真正“长期”的项目级记忆层**——

- 它不做通用 RAG，不帮你背文献；
- 它只老老实实记录：你和你的 copilot 在这个项目里  
  **做过什么、怎么做的、为什么这么做、下一步要做什么**。

换句话说：

> 让「未来的你 + 当前这轮大模型」  
> 能够一起接上「过去的你们」已经走过的路，  
> 而不是每次都从一片空白的对话框重新开始。


## 功能一览（TL;DR）

`research-memory` 是一个为学术研究项目设计的 Claude Code Skill / Python 工具，提供三件事：

1. **会话启动：`research_memory_bootstrap`**
   - 从 `memory/` 目录里拉取：
     - 项目概览（研究问题、假设、数据源…）
     - 最近 N 条 devlog
     - 当前 TODO 列表
   - 自动生成一份「最近进展 + 建议工作计划」

2. **会话记录：`research_memory_log_session`**
   - 将一段研究工作结构化写入：
     - `devlog.md`：按研究阶段（DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes）分块
     - `experiments.csv`：一行一个实验设定（hypothesis/dataset/model/metrics/notes…）
     - `decisions.md`：关键决策及其理由/备选方案
     - `todos.md`：新增 TODO，同时把完成的 TODO 勾选为 `[x]`

3. **历史查询：`research_memory_query_history`**
   - 支持按关键词 + 简单过滤（日期 / 阶段 / 类型）在：
     - `devlog.md`
     - `decisions.md`
     - `experiments.csv`
   中查找相关记录，并返回摘要 + key snippets。

**全部基于本地文本文件（Markdown + CSV），Git 友好，可手动编辑，无外部服务依赖。**

---

## 架构总览

整体结构：

```text
research-memory/
├── handlers.py        # Skill 的 Python 实现 & CLI 入口
├── SKILL.md           # Claude Code Skill 描述（tools 定义）
├── config/
│   └── config.json    # Skill 行为配置
├── .claude/
│   ├── CLAUDE.md      # 项目级指示，告诉 Claude 何时使用本 skill
│   └── settings.local.json  # Claude Code 本地设置示例
└── memory/            # 实际的「项目记忆层」（可自动创建）
    ├── project-overview.md  # 项目长期信息
    ├── devlog.md            # 开发/分析日志（按 session + 阶段）
    ├── decisions.md         # 关键决策记录
    ├── experiments.csv      # 实验表（结构化）
    └── todos.md             # TODO / open questions
````

核心组件：

* **Skill 层**

  * `SKILL.md` 定义了三个工具：

    * `research_memory_bootstrap`
    * `research_memory_log_session`
    * `research_memory_query_history`
  * 由 Claude Code 调用 `handlers.py` 中对应函数。

* **后端层**

  * `MemoryBackend` 封装所有文件读写、配置加载和 TODO 处理逻辑：

    * 现在是本地 Markdown + CSV；
    * 将来可以替换成 SQLite / 向量库 / MCP server，而不改外层接口。

---

## 安装

在 Claude Code 中，首先注册市场：

```bash
/plugin marketplace add syfyufei/research-memory
```

然后从市场安装插件：

```bash
/plugin install research-memory@research-memory-marketplace
```

### 验证安装

检查命令是否出现：

```bash
/help
```

```
# 应该看到 9 个命令：
# /research-memory:bootstrap - 恢复项目上下文并生成工作计划
# /research-memory:status - 快速查看项目状态
# /research-memory:remember - 记住当前工作会话
# /research-memory:query - 查询历史记录
# /research-memory:timeline - 可视化项目时间线
# /research-memory:summary - 生成完整项目摘要
# /research-memory:review - 回顾特定时间段的工作
# /research-memory:insights - 获取 AI 智能洞察和建议
# /research-memory:checkpoint - 创建项目状态检查点
```

### 快速开始

Research Memory 可以通过两种方式使用：

**方式 1：斜杠命令**

核心命令：
```bash
/research-memory:bootstrap    # 恢复项目上下文
/research-memory:status       # 快速状态概览
/research-memory:remember     # 记住当前会话
/research-memory:query        # 搜索历史记录
```

分析与报告：
```bash
/research-memory:timeline     # 显示项目时间线
/research-memory:summary      # 生成完整项目摘要
/research-memory:review       # 回顾特定时间段
/research-memory:insights     # 获取 AI 洞察
/research-memory:checkpoint   # 创建状态检查点
```

**方式 2：自然语言**

```
"Research Memory，帮我恢复一下项目状态"
"显示项目的快速状态"
"记住这次工作会话"
"搜索我们关于空间滞后模型的决策"
"生成一个项目摘要用于周会汇报"
```

Research Memory 会在首次使用时自动创建必要的 `memory/` 目录和文件。

### 卸载

**如果通过市场安装**：

```bash
claude plugin uninstall research-memory
```

**如果手动安装**：

```bash
# 从项目中删除技能文件
rm -f handlers.py config/config.json .claude/CLAUDE.md SKILL.md
rm -rf config/ .claude/ memory/
```

---

## 配置：`config/config.json`

所有行为都由一个 JSON 配置文件控制，默认配置长这样（节选）：

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

关键字段说明：

* `memory_directory`：记忆文件目录（相对项目根目录）；

* `encoding`：文件编码（默认 `utf-8`，也可以改成 `gbk` 等）；

* `timestamp_format`：

  * `"ISO8601"` → 例如 `2025-12-03T19:30:00+09:00`
  * `"YYYY-MM-DD_HH-MM-SS"` → 适合文件名 / 人眼阅读
  * `"timestamp"` → Unix 时间戳（秒）；

* `bootstrap.recent_entries_count`：启动时显示多少条最近 devlog；

* `logging.phase_sections`：支持的研究阶段标签；

* `logging.experiment_schema`：`experiments.csv` 中必须包含的字段；

* `search.*`：查询时返回结果数和是否附带上下文。

你可以按需要修改 `config.json`，所有配置项都已在 `MemoryBackend` 中生效。

---

## 在 Claude Code 中使用

### 典型调用场景

**1. 开始一天的工作：恢复上下文**

> 「帮我用 research-memory 恢复一下上次做到哪一步，并给一个今天的 plan。」

Skill 行为：

* 调用 `research_memory_bootstrap`：

  * 读取 `project-overview.md`（如果已经写过）；
  * 抽取最近 N 条 devlog（带 timestamp + 阶段信息）；
  * 汇总当前未完成 TODO；
  * 生成一个「今日工作建议计划」。

---

**2. 完成一个阶段：记录这次 session**

> 「这一段工作帮我整理成一条 research log，按 DGP / data_analyse / modeling 分段记到 research-memory 里。」

Claude 会：

1. 根据当前对话内容和你刚做的事情，构造一个 payload，例如：

   ```jsonc
   {
     "session_goal": "在 MCIB_v1.3 上跑空间 DiD，验证 H2",
     "changes_summary": [
       "更新 01_clean_mcib.R，增加 treat_window_180 变量",
       "过滤样本数 < 100 的自治市"
     ],
     "phases": {
       "DGP": "假定处理效应在 0–180 天内逐渐显现，使用距离阈值 50km 构造权重矩阵。",
       "data_analyse": "绘制处理组/对照组 baseline 期认知均值对比图，未见明显 pre-trend 交叉。",
       "modeling": "估计两类规约：TWFE + cluster by municipality；加入省级时间趋势的扩展规约。",
       "robustness": "简单 placebo：将处理时间整体平移 1 年，结果不显著。"
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
         "notes": "结果对窗口设定较敏感，需要进一步稳健性检验。"
       }
     ],
     "decisions": [
       {
         "title": "暂定 Model B 为主规约",
         "rationale": "加入省级时间趋势后 pre-trend 更平稳，系数更稳定。",
         "alternatives": [
           "继续使用简单 TWFE 作为主规约",
           "尝试 event-study 形式"
         ]
       }
     ],
     "todos": [
       "增加基于 k-nearest neighbors 的空间权重矩阵对比",
       "系统整理 placebo / alternative spec 结果写入 paper.qmd"
     ],
     "completed_todos": [
       "在 Methods 部分补充空间权重矩阵构造说明"
     ]
   }
   ```

2. 调用 `research_memory_log_session(payload)`，自动：

   * 在 `devlog.md` 里追加一条带 timestamp 的 Session 记录；
   * 在 `experiments.csv` 里插入一行完整的实验信息；
   * 在 `decisions.md` 中写入决策块；
   * 在 `todos.md` 里追加新 TODO，并将 `completed_todos` 中的事项标记为完成。

之后，你只需要自然描述「刚才做了什么」，Skill 会帮你把它变成可以长期检索的结构化记忆。

---

**3. 回顾历史：查看过去的决策和实验**

> 「我们之前为什么放弃过空间 lag 模型？」
> 「查一下 H2 做过的所有实验。」
> 「看下关于 hksarg_parser.R 的修改记录。」

此时 Claude 会调用：

```python
query_history(query, filters=None)
```

Skill 会：

* 在 `devlog.md` / `decisions.md` / `experiments.csv` 中做关键词匹配；
* 按配置返回最多 `search.max_results` 条匹配；
* 附上必要的上下文（前后若干行）；
* 生成一个简短摘要，告诉你：

  * 当时的决策是什么；
  * 哪些实验做过；
  * 哪些替代表达/设定被放弃了。

---

## 命令行使用（可选）

除了通过 Claude Code 调用，你也可以在命令行直接操作 `handlers.py`——适合你临时没开 Claude，或者想用脚本批量处理。

### 1. Bootstrap

```bash
python handlers.py bootstrap
```

输出一个 JSON，包含：

* `project_context`
* `recent_progress`
* `current_todos`
* `work_plan_suggestions`
* `timestamp`

### 2. 记录 Session

```bash
python handlers.py log-session \
  --payload-json '{
    "session_goal": "测试 CLI 日志",
    "changes_summary": ["更新 README 示例"],
    "phases": {"notes": "第一次在命令行用 research-memory"},
    "todos": ["在 paper.qmd 中引用这个工具"]
  }'
```

### 3. 查询历史

```bash
# 最简单：按关键词搜索
python handlers.py query --question "空间 lag 模型"

# 带过滤：时间 + 阶段 + 类型
python handlers.py query \
  --question "H2" \
  --from-date 2025-01-01 \
  --to-date 2025-12-31 \
  --phase modeling \
  --type experiments \
  --limit 5
```

CLI 会输出 JSON，方便你在其他脚本里继续使用。

---

## 文件格式示例

### `memory/devlog.md`

```markdown
# Development Log

## 2025-12-03 10:15

**Session Goal**: 在 MCIB_v1.3 上跑空间 DiD，验证 H2

**Changes Summary**:
- 更新 01_clean_mcib.R，增加 treat_window_180 变量
- 过滤掉样本数 < 100 的自治市

### DGP
假定处理效应在 0–180 天内逐渐显现，使用 50km 阈值构造二值空间权重矩阵并行标准化。

### data_analyse
绘制处理组与对照组 baseline 期认知均值对比，未见明显 pre-trend 交叉。

### modeling
估计两类规约：Model A (TWFE)、Model B (TWFE + 省级时间趋势)，H2 系数在两类模型中方向一致。

### robustness
做了简单 placebo 检验（处理时间整体平移一年），效果不显著。

### notes
需要进一步尝试 event-study 和不同空间权重矩阵。

---

```

### `memory/experiments.csv`（表头示意）

```csv
timestamp,experiment_id,hypothesis,dataset,model,metrics,notes,research_phase
2025-12-03T10:15:00+09:00,exp_20251203_101500,H2,MCIB_v1.3,"Spatial DiD, W=50km",{"ATT":0.153,"p_value":0.021},"placebo 结果不稳","DGP,data_analyse,modeling,robustness"
```

### `memory/todos.md`

```markdown
# Project TODOs

- [ ] 增加基于 k-nearest neighbors 的空间权重矩阵对比
- [x] 在 Methods 部分补充空间权重矩阵构造说明 (completed: 2025-12-03 - via log_session)
```

### `memory/decisions.md`

```markdown
# Key Decisions

## 2025-12-03 10:20 — 暂定 Model B 为主规约

**Decision**  
使用带省级时间趋势的 TWFE 作为主规约。

**Rationale**  
pre-trend 更平稳，估计结果在不同子样本中更稳定。

**Alternatives**  
- 保持简单 TWFE 为主规约  
- 改用 event-study + group-specific trends
```

---

## 设计原则

* **Local-first**：所有东西都是本地文本文件，可 Git 管理、可手动编辑；
* **Skill-first**：Claude Code 通过 skill 工具调用，不需要你关心具体文件路径；
* **可扩展**：通过 `MemoryBackend` 抽象层，将来可以无缝换成数据库 / MCP / 远程服务；
* **语义对齐科研工作流**：

  * DGP / data_preprocess / data_analyse / modeling / robustness / writing / infra / notes
  * 而不是只写几句「今天改了点代码」。

---

## Roadmap

当前版本是 **v0.x（文件后端版）**，后续可能会考虑：

* 支持 SQLite / DuckDB 作为后端（更强查询能力、支持聚合分析）；
* 增加向量检索，对长 devlog 提供模糊匹配；
* MCP / HTTP 服务模式，可被多个项目 / Agent 共用；
* 多人协作场景下的锁定与合并策略。

---

## License & 作者

* **License**: MIT
* **Author**: Yufei Sun (Adrian) `<syfyufei@gmail.com>`
* **Repo**: [https://github.com/syfyufei/research-memory](https://github.com/syfyufei/research-memory)

---

如果你常常在几个大项目之间来回切换，
又不想每次都花半天时间“回忆昨天的自己在想什么”，
可以试着把 `research-memory` 装进你的研究仓库——
让 Claude Code 成为一个**真正记得整个项目历史**的搭档，而不是一个只记住当前对话的聊天对象。

```
::contentReference[oaicite:0]{index=0}
```
