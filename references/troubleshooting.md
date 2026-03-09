# OPC 故障排查与问题归因

## 问题归因原则

OPC 编排中遇到问题时，必须先归因再修复。问题来源三层：

| 层 | 来源 | 典型问题 | 如何判断 |
|----|------|---------|---------|
| L1 | **OpenClaw 平台** | sub-agent 不 announce、spawn 失败、session 超时 | 换一个最简 task 测试，如果也失败则是 L1 |
| L2 | **OPC 编排 Skill** | 角色定义不清导致产出偏离、依赖管理错误、成本追踪遗漏 | task 正常完成但产出不符合预期 |
| L3 | **业务 Skill** | gundam-ops 操作失败、API 认证过期、组件版本不匹配 | spawn 成功、编排正确，但具体操作步骤报错 |

**归因决策树**：
```
sub-agent 没有结果？
├── spawn 返回 error → L1：OpenClaw 平台问题
├── spawn accepted 但无 announce
│   ├── subagents list 显示 active → 还在运行，等待
│   ├── subagents list 显示 done → L1：announce 机制问题
│   │   → 缓解：主动 sessions_history 拉取结果
│   └── subagents list 显示 error → 检查错误
│       ├── task 内容有语法错误 → L2：prompt 问题
│       └── 工具调用失败 → L3：业务 Skill 问题
│
sub-agent 有结果但不符合预期？
├── 完全跑偏（角色没理解） → L2：角色卡定义不清
├── 方向对但质量差 → L2：task 描述不够具体
├── 方向对但操作报错 → L3：业务 Skill 问题
└── 方向对质量好但格式不对 → L2：产出要求不明确
```

## 已知问题与缓解方案

### P1: Sub-agent 不 announce（高频）

**现象**：sub-agent 完成任务（subagents list 显示 done），但 Main Session 收不到 announce。

**根因**：OpenClaw 平台的 announce 机制在某些情况下不触发（可能与 context 大小、model 切换有关）。

**缓解策略（写入编排流程）**：

```
CEO 编排流程中必须加入「主动检查」步骤：

1. spawn sub-agent
2. 等待合理时间（根据任务复杂度：简单 2min，中等 5min，复杂 10min）
3. 如果收到 announce → 正常流程
4. 如果未收到 announce → 执行主动检查：
   a. subagents(action=list) 查看状态
   b. 如果 done → sessions_history 拉取结果
   c. 如果 active → 继续等待
   d. 如果 error → 分析原因，决定重试或调整
```

**关键：不要假设 announce 一定会到达。每个 spawn 后都应有超时检查机制。**

### P2: Sub-agent 使用了错误的 model

**现象**：sub-agent 被分配到能力较弱的 model，导致产出质量差或无法完成复杂任务。

**缓解**：在 sessions_spawn 时可指定 model 参数。

### P3: Sub-agent 超时

**现象**：sub-agent 长时间无响应。

**缓解**：设置 runTimeoutSeconds 参数。

## CEO 编排最佳实践

### 1. 每次 spawn 后设置检查点

不要 spawn 完就忘记。CEO 的工作循环应该是：

```
spawn → 记录（tracker update assigned）
       → 等待 announce OR 超时检查
       → 收到结果 → 验证质量
       → 更新状态（tracker update completed/failed）
       → 触发下游
```

### 2. 保持 tracker 与实际状态同步

每次状态变更都通过 project_tracker.py 记录。

### 3. 失败时快速归因

用上面的归因决策树，3 步内确定问题层：
1. spawn 成功吗？→ 不成功=L1
2. 产出有吗？→ 没有且 done=L1 announce问题
3. 产出对吗？→ 不对=L2(编排) 或 L3(业务)
