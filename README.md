# 🏢 OPC — One-Person Company

> **Multi-Agent Orchestration Skill** — Turn OpenClaw into the CEO of a one-person company.
>
> **多 Agent 编排技能** — 让 OpenClaw 成为一人公司的 CEO。

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### What is OPC?

OPC (One-Person Company) is an OpenClaw skill that turns complex tasks into multi-agent collaboration. You give the goal, the CEO (OpenClaw) breaks it down, hires the right agents, monitors progress, and delivers results.

```
You (Owner) → OpenClaw CEO → Sub-agents (Specialists)
```

### Key Features

- **Phase 0 Context Intake** — CEO reads your background, proposes a plan, waits for confirmation before executing
- **Built-in Persona Library** — Inject top expert mindsets (Kotler, Fowler, Jeff Dean...) into each agent role
- **LZW Advisor Persona** — Author's own methodology framework, ready to inject into any agent role
- **Project State Persistence** — Survives context compaction; full lifecycle state in `state.json`
- **Checkpoint & Resume** — Failed agents resume from last checkpoint, not from scratch
- **Auto Root Cause Analysis** — L1-L4 fault classification (platform / orchestration / skill / external)
- **Aware Triggers** — Declarative event-driven scheduling (cron / once / interval / on_message)
- **Tool Discovery v2** — domain × capability tag system, precise skill recommendations
- **User Model Evolution** — CEO writes back learnings after each project; gets smarter over time

### Quick Start

```bash
# Install
cd ~/.openclaw/skills
unzip agent-orchestration-v3.2.zip

# Trigger OPC by telling OpenClaw:
# "Help me build a complete [project]"
# "I need [multi-step task] done end-to-end"
```

### Architecture

```
agent-orchestration-20260309-lzw/
├── SKILL.md              ← Entry point (v3.2)
├── brain/                ← CEO decision layer
│   ├── core-flow.md      ← 4-phase flow + Context Intake
│   ├── task-decomposition.md
│   ├── role-design.md
│   └── collaboration-patterns.md
├── engine/               ← Execution engine
│   ├── project_state.py  ← Project lifecycle state
│   ├── trigger_engine.py ← Aware triggers
│   ├── tool_discovery.py ← Tool discovery (tag system v2)
│   └── diagnose_agent.py ← Auto root cause analysis
└── playbook/             ← Knowledge & templates
    ├── persona-priming.md     ← Persona methodology + library index
    ├── personas/
    │   └── lzw.md             ← Built-in LZW Advisor Persona (v3.2)
    ├── templates/
    └── scenarios/
```

### Persona Priming

Two types of Personas, two design logics:

| Type | Example | How it works |
|------|---------|-------------|
| **Activation** (public figures) | Kotler, Fowler, Jeff Dean | One-line reference activates LLM's pre-trained knowledge |
| **Injection** (real individuals) | LZW (`personas/lzw.md`) | Full methodology doc injected into agent context |

**New paradigm**: You can crystallize your own thinking framework into a Persona and inject it into your agent team.

### Real-World Validation

| Case | Scale | Result |
|------|-------|--------|
| 315 Marketing Campaign (v1.0) | 3 agents serial | 67K tokens / $0.17 |
| 3 Venues Parallel Build (v1.4) | 4 agents parallel | All 3 venues delivered |
| KangaBase 0→1 (v2.0) | 8 agents, 4 phases | ~100 files / 8000 lines in 8h |
| Neurotech Deep Analysis (v3.1) | 4 researchers + integrator | 4500-word report / $0.10 |

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
- Python 3 (for engine scripts)

### License

Apache License 2.0 — modifications must declare changes. See [LICENSE](LICENSE).

---

<a name="中文"></a>
## 中文

### OPC 是什么？

OPC（One-Person Company，一人公司）是一个 OpenClaw Skill，把复杂任务转化为多 Agent 协作。你说目标，CEO（OpenClaw）负责拆活儿、招人、盯进度、交结果。

```
用户（老板）→ OpenClaw CEO → Sub-agents（专业员工）
```

### 核心能力

- **Phase 0 Context Intake** — CEO 理解背景，给出方案，等确认后才执行
- **内置 Persona 库** — 给角色注入 Kotler / Fowler / Jeff Dean 等顶级人才的方法论
- **LZW 顾问 Persona** — 作者本人的方法论框架，可直接注入任意 Agent 角色
- **项目状态持久化** — 抗 context compaction，全生命周期状态写入 `state.json`
- **断点续传** — Agent 失败后从断点继续，不完全重跑
- **自动归因** — L1-L4 故障分层（平台/编排/Skill/外部）
- **Aware 触发器** — 声明式事件驱动（cron / once / interval / on_message）
- **工具发现 v2** — domain × capability 双轴标签，精准推荐可用 Skill
- **用户模型自进化** — 每次项目结束 CEO 自动写回学习结果，越用越懂你

### 快速上手

```bash
# 安装
cd ~/.openclaw/skills
unzip agent-orchestration-v3.2.zip

# 触发 OPC，对 OpenClaw 说：
# "帮我做一个完整的 [项目]"
# "我需要 [多步骤任务] 全链路完成"
```

### Persona Priming

OPC 的 Persona 分为两类，设计逻辑不同：

| 类型 | 代表 | 工作原理 |
|------|------|---------|
| **激活型**（公众人物） | Kotler、Fowler、Jeff Dean | 一行描述即可激活 LLM 预训练知识 |
| **注入型**（真实个人） | LZW（`personas/lzw.md`） | 完整方法论文档注入 Agent context |

**新范式**：用户可以把自己的思维框架沉淀为 Persona，注入到自己的 Agent 团队中。

### 实战验证

| 案例 | 规模 | 结果 |
|------|------|------|
| 315 营销活动（v1.0） | 3 角色串行 | 67K tokens / $0.17 |
| 三会场并行搭建（v1.4） | 4 角色并行 | 3 个会场全部交付 |
| KangaBase 从零到开源（v2.0） | 8 Agent / 4 Phase | ~100文件/8000行，8小时 |
| 神经调控深度分析（v3.1） | 4 研究员 + 整合员 | 4500字报告 / $0.10 |

### 版本历史

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| **v3.2** | **2026-03-16** | **内置 LZW 顾问 Persona + personas/ 目录** |
| v3.1 | 2026-03-14 | 用户模型自学习：Phase 0 读取 + Phase 4 写回 |
| v3.0 | 2026-03-14 | 三层架构重构 + Context Intake + 工具发现标签体系 v2 |
| v2.0 | 2026-03-12 | Aware 触发器 + 运行时工具自发现 |
| v1.4 | 2026-03-11 | 状态持久化 + 断点续传 + 自动归因 |
| v1.0 | 2026-03-09 | 首版：角色卡 + 任务分解 + 协作模式 |

见完整 [CHANGELOG.md](CHANGELOG.md)

### 前置条件

- 已安装并配置 [OpenClaw](https://github.com/openclaw/openclaw)
- Python 3（用于引擎脚本）

### 许可证

Apache License 2.0 — 修改文件须声明变更。详见 [LICENSE](LICENSE)。

---

*Built with ❤️ by LZW · Powered by [OpenClaw](https://github.com/openclaw/openclaw)*
