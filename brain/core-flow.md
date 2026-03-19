# OPC 核心执行流程

> CEO 决策层 — 完整的 OPC 工作循环

---

## Phase 0：Context Intake（上下文摄入）⭐ 最重要

**OPC 被触发后，第一步必须是理解背景、任务和目标，给出推进方案，征询确认。**

不允许跳过此步骤直接开始规划。

### 0.1 用户模型读取（Phase 0 第一步，在追问用户之前）

CEO 必须依次尝试读取以下文件（存在就读，不存在跳过，不报错）：

```
优先级  文件                                            说明
①      workspace/opc-user-model.md                    OPC 专属用户模型（越用越精准）
②      ~/.openclaw/workspace/MEMORY.md                OpenClaw 官方长期记忆
③      ~/.openclaw/workspace/USER.md                  用户扩展文件（可能不存在）
④      ~/.openclaw/workspace/memory/YYYY-MM-DD.md     今日日志（可选，近期上下文）
```

读取后，CEO 综合这些信息形成对用户的预判：
- 用户的偏好和风格（深度 vs 广度、报告格式偏好等）
- 过去类似任务的成功配置（角色数量、Persona 选择、大致 token 消耗）
- 已知约束（平台限制、惯用工具等）

**有预判 → 生成带预填的方案草稿，用户只需校正差异**
**无预判（首次）→ 正常追问，记录为这是第一次使用**

### 0.2 主动追问框架

CEO 围绕以下维度明确信息（已从用户模型中推断的可跳过，不确定的主动问）：

```
【背景】
- 这个任务在什么业务场景下？有什么前置条件？
- 是新建还是继续已有工作？

【目标】
- 最终交付物是什么？（文档/页面/代码/分析报告...）
- 成功的标准是什么？怎么判断"完成了"？

【约束】
- 截止时间？预算（token 上限）？
- 有哪些平台限制（需要 SSO/浏览器/特定工具）？
- 需要人工介入的节点？

【范围】
- 从哪里开始、到哪里结束？
- 哪些不在本次范围内？
```

### 0.3 推进方案输出格式

理解完成后，CEO 输出以下结构化方案，**等用户确认后才进入 Phase 1**：

```markdown
## 📋 OPC 项目方案

**背景理解**：{一句话概括}
**目标**：{交付物 + 成功标准}
**约束**：{时间/预算/限制}

**推进方案**：
- 角色配置：{N 个角色，名称 + 主要职责}
- 协作模式：{串行/并行/混合，简述顺序}
- 预估总预算：~{N}K tokens
- 预计耗时：~{N} 分钟

**确认后开始执行，是否有需要调整的地方？**
```

### 0.3 复杂度自动判断

| 条件 | 复杂度 | 确认轮次 |
|------|--------|---------|
| ≤2 角色，单一流水线 | 简单 | 1轮（合并 0+1） |
| 3-5 角色，有并行 | 中等 | 1轮（0+1合并）|
| >5 角色，跨业务线，>200K预算 | 复杂 | 2轮（0理解→1方案）|

---

## Phase 1：项目规划

1. 用 `project_state.py init` 创建项目
2. 拆解 OKR → Epic → Task（见 task-decomposition.md）
3. 定义角色、依赖关系、token 预算
4. 工具扫描（可选，见 engine/README.md）
5. **用户确认方案后才执行**

```bash
python3 engine/project_state.py init "项目名称"
python3 engine/project_state.py update-phase <pid> phase_1_planning
```

---

## Phase 2：团队组建

按角色定义 spawn Sub-agents，注入角色卡 + Heartbeat 协议。

```bash
python3 engine/project_state.py agent-start <pid> <label> '{"role":"角色名"}'
```

每个 spawn 后必须给用户一条确认消息：
> ✅ {角色} 已启动（预计 N 分钟），持续监控中。

---

## Phase 3：执行监控循环

```
Sub-agent 完成 / 超时检查
    │
    ├── 收到结果 → 质量验收
    │   ├── OK → agent-complete → 触发下游
    │   └── 不OK → sessions_send 修改 → 最多 3 次
    │
    ├── 超时未收到 → 主动检查
    │   subagents(action=list) → sessions_history → 拉取结果
    │
    ├── 触发器评估（每轮循环必须执行）
    │   python3 engine/project_state.py trigger-evaluate <pid>
    │
    └── 阶段进度汇报给用户
```

### 主动监控间隔

| 任务复杂度 | 首次检查 | 后续间隔 |
|-----------|---------|---------|
| 简单 | 3 min | 2 min |
| 中等 | 5 min | 3 min |
| 复杂 | 10 min | 5 min |

---

## Phase 4：交付汇总

1. 汇总所有 Sub-agent 产出
2. 生成成本报告：`python3 engine/project_state.py cost <pid>`
3. 关闭项目：`python3 engine/project_state.py close <pid>`
4. 向用户交付最终成果 + 成本报告

---

## 关键规则（CEO 必须遵守）

1. **Context Intake 不可跳过** — Phase 0 是所有 OPC 项目的入口，必须执行
2. **确认后才执行** — 任何 spawn 必须在用户确认方案后才触发
3. **不信任 announce** — 超时必须主动检查
4. **每步持久化** — Phase 切换、agent 状态变更立即写入 project_state
5. **断点优于重试** — agent 失败先保存 checkpoint，再考虑重新 spawn
6. **Phase 3 必须 trigger-evaluate** — 每轮监控循环必须调用触发器评估

---

## 用户模型更新规范（Phase 4 关闭前必须执行）

项目关闭前，CEO 将本次项目的关键信息写入 `workspace/opc-user-model.md`：

### 写入内容

```markdown
## [YYYY-MM-DD] {项目名称}（{项目ID}）

- 任务类型：{research / marketing / engineering / content / ...}
- 角色配置：{N 个角色，列出名称+职责}
- 协作模式：{串行 / 并行 / 混合}
- 实际消耗：{N}K tokens（预算 {N}K）
- 耗时：{N} 分钟
- 结果：{✅ 成功 / ⚠️ 部分完成 / ❌ 失败}
- Persona 效果：{哪个 Persona 表现突出，简短备注}
- 踩坑 / 经验：{有就写，没有跳过}
```

### 更新用户偏好区

如果本次项目揭示了用户的新偏好或修正了旧认知，同步更新文件顶部的 `## 用户偏好` 区块。

### 写入原则

- **只追加，不删除历史记录**
- **偏好区可更新**（覆盖旧的同类条目）
- **不写入 MEMORY.md 或 USER.md**（那是用户和喵神维护的，OPC 不动）
- **文件不存在时自动创建**（参考模板：`playbook/templates/opc-user-model.md`）



---

## Phase 0 扩展：问题重构（Office Hours）— v5.3 新增

> 灵感来源：gstack `/office-hours`（Garry Tan，YC CEO）
> 触发条件：L2/L3 任务必须执行；L1 可选

在 Context Intake 完成后，CEO 在开始规划前先执行问题重构：

### 三步问题重构

```
Step 1：听痛点，不听功能描述
  ❌ 用户说"做一个 X" → 直接规划 X
  ✅ 先问："你遇到了什么具体问题？什么情况下最让你烦？"
  目标：找到用户真正想解决的问题，而不是他描述的功能

Step 2：挑战前提假设（Premise Challenge）
  提出 2-4 条关于这个任务的核心假设，让用户逐条确认：
  "我理解你的核心需求是 A，B 是必须要做的，C 可以之后再加——对吗？"
  用户同意/修正每一条 → 这些假设成为规划的基础

Step 3：提供 2-3 个实现路径 + 诚实工作量估算
  每条路径：
  - 一句话描述做什么
  - 预计 token 消耗（S/M/L/XL）
  - 核心权衡（速度 vs 质量 vs 完整性）
  推荐最小可行路径（先跑起来，再迭代）
```

### 何时可以跳过

```
✅ 可跳过：
  - 用户已明确表达完整需求（有具体文件、路径、标准）
  - L1 轻量任务（< 3步，单一领域）
  - 重复型任务（之前做过完全相同的事）

❌ 不可跳过：
  - 用户描述的是"症状"而不是"需求"
  - 任务描述模糊或宏大（"帮我做完整的X"）
  - L3 重型任务（跨天/多领域）
```

### 输出格式

```
🔍 问题重构

真实需求（我的理解）：{一句话，不同于用户的原始描述时要标注}

核心假设确认：
  A. {假设}  → 请确认
  B. {假设}  → 请确认

推荐路径：{路径名}（预计 ~{N}K tokens）
  理由：{为什么这个路径最合适}

备选路径：
  - {路径B}（{工作量}，适合{场景}）
  - {路径C}（{工作量}，适合{场景}）

等你确认后开始规划。
```

---

## Phase 4：交付包 Delivery Package（v5.0 新增）

> CEO 在所有 Agent 完成 + verify 通过后，**主动生成交付包**，不等用户追问。
> 交付包是 OPC 与用户之间的最后一公里——从"原材料"变成"可以用的结果"。

### 标准交付包格式

```
📦 OPC 项目交付
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 核心结论
{一段话，直接说这个项目做出了什么、结论是什么}

📁 产出清单
- {label}：{path} — {一句话描述这个文件是什么}
- ...

💡 CEO 建议
{基于产出，下一步可以做什么？有没有值得继续深入的方向？}

⚠️ 注意事项
{质量瑕疵（如有）/ 未完成项 / 需要人工确认的地方}
{如无，填"无"}

💰 消耗摘要
总 token：~{N}K | 耗时：~{N} 分钟 | Agent 数量：{N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 生成规则

- **核心结论**：不是产出列表，是真正的"所以怎样"——即使用户不读报告，看这一段也能做决策
- **CEO 建议**：至少给 1 条下一步建议，不能只说"供参考"
- **注意事项**：诚实写出瑕疵，不粉饰太平；没有瑕疵才写"无"
- **自适应长度**：L1 任务交付包可以压缩到 5 行；L3 任务完整展开

---

## Phase 5：自动复盘 Retrospective（v5.0 新增）

> 项目 close 时自动触发，**不需要 spawn Sub-agent**，CEO 自己执行。
> 目的：把踩过的坑变成系统知识，让 OPC 越用越强。

### 触发时机

```bash
# close 命令自动触发 Phase 5
python3 engine/project_state.py close <pid> "项目已交付"
# close 内部会自动调用 retrospective 逻辑
```

### 复盘五步

```
Step 1：消耗对比
  预估 token vs 实际 token
  偏差 > 50% → 记录原因到 state.json

Step 2：验收失败归因
  有 verify 失败记录？→ 提炼失败模式 → 写入 opc-user-model.md
  "研究员 A 在 X 类任务上需要更明确的格式约束"

Step 3：质量自评
  CEO 给本次产出打分（1-5）
  评分依据：用户满意度信号 + verify 通过率 + 交付包完整度

Step 4：一句话教训
  这个项目最重要的一个教训是什么？
  写入 playbook/scenarios/{场景}.md 的「踩坑记录」区块

Step 5：更新用户模型
  把任务类型、角色配置、有效 Persona、消耗、评分写回 opc-user-model.md
```

### 复盘产出写入位置

| 内容 | 写入位置 |
|------|---------|
| 消耗偏差原因 | opc-projects/{pid}/state.json → retrospective |
| 失败模式 | opc-user-model.md → failure_patterns |
| 质量评分 | opc-projects/{pid}/state.json → quality_score |
| 一句话教训 | playbook/scenarios/{type}.md → 踩坑记录 |
| 全量项目记录 | opc-user-model.md → project_history |
