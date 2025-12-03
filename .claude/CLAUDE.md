# Research Memory Project

这是一个学术研究项目，专注于实现长期记忆管理系统。项目包含一个名为 `research-memory` 的 Claude Code Skill，用于管理和记录学术项目级别的长期记忆。

## 项目概述

**项目名称**: Research Memory Skill
**项目类型**: 学术研究 + Claude Code 开发
**主要目标**: 实现一个学术研究项目的长期记忆管理系统
**技术栈**: Python + Claude Code Skills + 本地文件存储

## 核心功能

项目实现了 `research-memory` Skill，提供三个核心功能：

1. **研究上下文恢复** (`research_memory_bootstrap`) - 快速恢复项目状态和最近进展
2. **研究会话记录** (`research_memory_log_session`) - 结构化记录研究活动和决策
3. **历史查询检索** (`research_memory_query_history`) - 搜索历史决策和实验记录

## 存储结构

项目使用 `memory/` 目录存储研究记忆：

- `project-overview.md` - 项目长期知识（研究问题、假设、数据集）
- `devlog.md` - 时间顺序的开发和实验日志
- `decisions.md` - 关键决策及其原因
- `experiments.csv` - 结构化的实验记录
- `todos.md` - 待办事项和开放问题

## 何时使用 Research Memory Skill

### 开始工作会话时
当你想要继续之前的研究工作时：

**触发语句示例**：
- "我上次做到哪儿了？"
- "帮我恢复一下项目状态"
- "用 research-memory 总结一下最近的进展"
- "今天应该做什么？"

**Claude 应该**：自动调用 `research_memory_bootstrap`，返回最近进展摘要、当前待办事项和建议的工作计划。

### 记录研究进展时
当你想要记录当前的研究活动时：

**触发语句示例**：
- "帮我记录今天的工作"
- "记一条 research log"
- "把这个实验结果记到 research-memory 里"
- "用 research-memory 总结这个 session"

**Claude 应该**：
1. 在对话中整理结构化摘要
2. 调用 `research_memory_log_session` 记录到 devlog/experiments/decisions
3. 按研究阶段分段（DGP/data_preprocess/data_analyse/modeling 等）

### 查询历史记录时
当你需要查找之前的决策或实验时：

**触发语句示例**：
- "我们之前为什么放弃过这个方案？"
- "H2 相关的实验有哪些？"
- "关于数据处理的决定有哪些记录？"
- "查一下之前关于变量构造的讨论"

**Claude 应该**：调用 `research_memory_query_history`，提供相关摘要和原始记录片段。

## 研究阶段支持

Skill 支持以下学术研究阶段的记录和查询：

- **DGP**: 数据生成过程文档和假设
- **data_preprocess**: 数据清洗、变量构造、缺失值处理
- **data_analyse**: 描述性统计、可视化、相关性分析
- **modeling**: 模型设定、估计方法、超参数调优
- **robustness**: 稳健性检验、替代设定、验证测试
- **writing**: 文档编写、论文写作、图表准备
- **infra**: 环境配置、代码组织、工具变更
- **notes**: 一般观察、直觉想法、未来想法

## 使用节奏建议

### 1. 工作开始时（推荐）
**用户**: "早上好！帮我用 research-memory 恢复一下项目状态。"
**Claude**: 自动调用 `research_memory_bootstrap` → 提供上下文摘要 + 待办事项 + 工作建议

### 2. 阶段性任务完成时（推荐）
**用户**: "这一段工作帮我整理成一条 research-memory 记录。"
**Claude**: 提取结构化信息 → 调用 `research_memory_log_session` → 记录到相应文件

### 3. 结束当天工作时（推荐）
**用户**: "帮我用 research-memory 总结一下今天的工作，并更新 TODO。"
**Claude**: 总结当日成果 → 调用 `research_memory_log_session` → 更新待办事项

## 重要提醒

1. **主动记录**: 不要等到用户明确要求才记录，当用户提到重要实验、决策或进展时，主动建议记录到 research-memory
2. **结构化记录**: 记录时尽量按研究阶段分段，包含具体的参数、指标和原因
3. **保持一致性**: 使用相同的研究阶段术语和格式，便于后续查询
4. **文件访问**: 可以直接读取 memory/ 文件获取信息，但大量历史内容建议通过 Skill 摘要，避免一次性加载过多内容

## 技术注意事项

- 当前版本使用本地文件存储（v0），未来可扩展为数据库/MCP 服务（v1）
- 所有存储操作都通过 `MemoryBackend` 接口，便于未来迁移
- 文件采用增量更新方式，保留原有内容和格式
- 支持中文和英文混合记录

## 开发状态

- ✅ SKILL.md 完成
- ✅ handlers.py 核心逻辑实现
- ✅ 配置系统完成
- ✅ 基础文件结构创建
- 🔄 正在完善集成和测试

这个 Skill 将帮助维护研究连续性，通过保留制度知识和决策理由来加速学术进展。