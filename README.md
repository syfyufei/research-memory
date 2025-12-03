# Research Memory Skill

一个为学术研究项目设计的 Claude Code Skill，用于管理和记录项目级的长期记忆，帮助研究人员在不同会话之间保持上下文连续性。

## 项目概述

这个 Skill 解决了学术研究中的一个核心问题：如何有效地记录和管理研究过程中的知识、决策和实验轨迹，以便在项目中断后能够快速恢复上下文，避免重复性工作。

## 核心功能

### 1. 研究上下文恢复 (`research_memory_bootstrap`)
快速恢复项目状态，包括：
- 最近的研究进展摘要
- 当前的待办事项
- 基于历史记录的工作建议

**使用示例**：
```
"帮我用 research-memory 恢复一下上次做到哪一步"
"今天的研究计划是什么？"
```

### 2. 研究会话记录 (`research_memory_log_session`)
结构化记录研究活动，支持：
- 按研究阶段分组的记录（DGP、数据预处理、建模等）
- 实验结果的系统化存储
- 决策理由和备选方案记录
- 自动化的 TODO 管理

**使用示例**：
```
"把今天的工作记到 research-memory 里"
"记录刚才这个实验的结果"
"帮我总结这个 session 并更新 TODO"
```

### 3. 历史记录查询 (`research_memory_query_history`)
高效检索历史信息：
- 关键词搜索（支持中文和英文）
- 按研究阶段筛选
- 跨文件综合搜索

**使用示例**：
```
"我们之前为什么放弃过空间 lag 模型？"
"H2 相关的实验有哪些？"
"关于变量构造的讨论记录"
```

## 支持的研究阶段

- **DGP**: 数据生成过程文档和假设
- **data_preprocess**: 数据清洗、变量构造、缺失值处理
- **data_analyse**: 描述性统计、可视化、相关性分析
- **modeling**: 模型设定、估计方法、超参数调优
- **robustness**: 稳健性检验、替代设定、验证测试
- **writing**: 文档编写、论文写作、图表准备
- **infra**: 环境配置、代码组织、工具变更
- **notes**: 一般观察、直觉想法、未来想法

## 文件结构

```
research-memory/
├── SKILL.md                          # 技能定义和主要实现
├── handlers.py                       # Python 核心逻辑
├── README.md                         # 项目说明
├── config/
│   └── config.json                   # 配置文件
├── .claude/
│   └── CLAUDE.md                     # Claude Code 项目说明
├── memory/                           # 研究记忆存储
│   ├── project-overview.md           # 项目概述
│   ├── devlog.md                     # 开发日志
│   ├── decisions.md                  # 关键决策记录
│   ├── experiments.csv               # 实验数据
│   └── todos.md                      # 待办事项
└── examples/                         # 使用示例（待完善）
```

## 快速开始

### 1. 安装和配置

项目不需要额外的依赖，只需要 Python 3.8+：

```bash
# 确保技能文件已正确创建
ls -la SKILL.md handlers.py config/

# 测试基础功能
python3 handlers.py bootstrap
```

### 2. 在 Claude Code 中使用

技能会自动被 Claude Code 识别。你可以通过自然语言触发：

#### 开始工作会话
```
用户: 早上好！帮我用 research-memory 恢复一下项目状态。
Claude: [自动调用 bootstrap 功能]
```

#### 记录研究进展
```
用户: 刚才的回归结果很好，帮我记录一下。
Claude: [自动提取信息并调用 log_session 功能]
```

#### 查询历史信息
```
用户: 我们之前讨论过数字化技能的测量方法吗？
Claude: [自动调用 query_history 功能]
```

### 3. CLI 使用

也可以直接通过命令行使用：

```bash
# 恢复项目上下文
python3 handlers.py bootstrap

# 查询历史记录
python3 handlers.py query --question "数字化技能"

# 记录会话（需要 JSON 格式的 payload）
python3 handlers.py log-session --payload-json '{"session_goal": "测试记录", "changes_summary": "创建示例文件"}'
```

## 配置选项

通过 `config/config.json` 可以自定义：

```json
{
  "bootstrap": {
    "recent_entries_count": 5,      // 恢复时显示的最近条目数
    "include_todos": true,          // 是否包含待办事项
    "suggest_work_plan": true       // 是否建议工作计划
  },
  "search": {
    "max_results": 10,              // 搜索最大结果数
    "include_context": true,        // 是否包含上下文
    "context_lines": 3              // 上下文行数
  }
}
```

## 技术特性

### v0 特点
- **本地文件存储**: 无需数据库，使用 Markdown + CSV
- **增量更新**: 保护已有内容，避免重复记录
- **中文支持**: 完全支持中英文混合记录
- **学术导向**: 针对学术研究工作流优化

### v1 预留扩展
- **数据库后端**: 可升级为 SQLite/PostgreSQL
- **向量搜索**: 支持语义搜索
- **MCP 集成**: 支持远程记忆访问
- **协作功能**: 多用户记忆共享

## 使用场景

### 个人研究者
- 在长时间项目中断后快速恢复上下文
- 避免重复性工作和决策遗忘
- 系统化记录实验和结果

### 研究团队
- 知识传递和决策追溯
- 避免重复性错误
- 维护团队的研究记忆

### 学术写作
- 方法论部分的结构化记录
- 实验结果的系统化管理
- 决策过程的完整追溯

## 示例工作流

### 每日开始研究
1. **触发**: "帮我恢复一下项目状态"
2. **获得**: 最近进展 + 当前 TODO + 工作建议
3. **开始**: 基于建议开始当天的工作

### 阶段性完成
1. **触发**: "记录这次实验结果"
2. **自动**: Claude 提取关键信息并结构化记录
3. **更新**: 自动更新 TODO 和实验记录

### 查询历史
1. **触发**: "我们为什么选择这个方法？"
2. **获得**: 决策理由 + 备选方案 + 相关实验
3. **继续**: 基于历史信息继续当前工作

## 开发状态

- ✅ 核心 SKILL.md 定义
- ✅ Python handlers.py 实现
- ✅ 配置系统
- ✅ 示例记忆文件
- ✅ 基础功能测试
- 📚 文档完善
- 📚 更多使用示例
- 📚 高级搜索功能

## 贡献指南

这个项目遵循标准的学术软件开发实践：

1. **代码质量**: 保持清晰的注释和文档
2. **测试覆盖**: 确保功能的正确性和稳定性
3. **用户友好**: 提供清晰的使用说明和示例
4. **向后兼容**: v0 到 v1 的平滑迁移路径

## 许可证

MIT License - 自由使用和修改

## 联系方式

- 作者: Yufei Sun (Adrian) <syfyufei@gmail.com>
- 项目地址: https://github.com/syfyufei/research-memory

---

这个 Skill 旨在帮助研究人员更好地管理和利用研究过程中的知识积累，提高学术研究的效率和质量。