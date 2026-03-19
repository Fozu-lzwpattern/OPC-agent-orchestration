# CEO 自主验收规则库 (v4.0)

> 每个 Phase 结束时，CEO **自己跑验收**——不依赖 Sub-agent 的自述。
> 验收通过才调用 `agent-complete`；不通过先反馈再重试，最多 3 次。

---

## 核心原则

**"Sub-agent 说完成了" ≠ "完成了"。CEO 必须独立核实。**

执行流程：
```
Sub-agent announce / 超时轮询到结果
    │
    ├── 1. 跑验收命令（见下方速查表）
    ├── 2. PASS → verify 命令记录 → agent-complete
    └── 3. FAIL → 发精准反馈 → 最多重试 3 次
                  第 3 次仍失败 → agent-fail + checkpoint → 告警用户
```

---

## 验收命令速查表

### 工程类

| 任务 | 验收命令 | 通过条件 |
|------|---------|---------|
| TypeScript/Node.js | `npm test` | 全绿，0 fail |
| Python | `python -m pytest` | 全绿 |
| 代码构建 | `npm run build` | 0 error |
| 文件存在 | `test -f <path> && wc -l <path>` | 存在 + 行数 > 阈值 |
| 接口可用 | `curl -s http://localhost:{port}/api/health` | 200 OK |

**工程类验收模板：**
```bash
# 1. 确认产出文件存在
ls -la <output_dir>
# 2. 跑测试
cd <repo> && npm test 2>&1 | tail -5
# 3. 关键文件内容抽查
head -20 <key_file>
```

### 研究/写作类

| 任务 | 验收方式 | 通过条件 |
|------|---------|---------|
| 研究报告 | `wc -l <file>` + 内容抽读 | 行数 > 50 + 关键章节存在 |
| 多角色汇总 | 检查各研究员输出文件均存在 | N 个文件全部存在且非空 |

**研究类验收模板：**
```bash
for f in <output_dir>/*.md; do
  echo "=== $f ===" && wc -l "$f" && head -5 "$f"
done
```

### 通用兜底验收（任何任务都适用）

```bash
# 文件存在性 + 大小
find <workspace> -newer <start_marker> -type f | head -20
# 读取产出尾部
tail -100 <output_file>
```

---

## 验收失败处理流程

```
验收失败（第 N 次）
    │
    ├── N < 3 → 发精准反馈给 Sub-agent
    │   "验收未通过（第{N}/3次）：
    │    ✗ {具体失败原因，附命令输出}
    │    请修复后重新提交。"
    │
    └── N = 3 → agent-fail + checkpoint 保存进度 + 通知用户
                人工判断：修复 skill → 断点续传 or 跳过
```

## 与 project_state.py 集成

```bash
# 验收（0=通过，非0=失败，自动记录到 state）
python3 engine/project_state.py verify <pid> <label> "npm test"

# 验收通过后再 complete
python3 engine/project_state.py agent-complete <pid> <label> \
  '{"output":"验收通过","verifyPassed":true}' <tokens>
```

---

## Phase 级汇总验收

Phase 切换时，CEO 执行：

```
1. 列出本 Phase 所有预期产出（from 项目规划）
2. 逐一核对：文件存在 + 内容抽查
3. 有缺失 → 补充 spawn 或标记 partial
4. 全部通过 → update-phase + 推送阶段成本报告（见 cost-tracking.md）
```


---

## Iron Law 调试协议（v5.3 新增）

> 灵感来源：gstack `/investigate` — "Iron Law: no fixes without investigation"

### 核心规则

**verify 失败不等于立刻重试。先调查，后修复。**

```
verify 失败第 1 次：
  → 仔细读错误信息
  → 确认是哪个 Agent 的产出问题（文件不存在？命令失败？）
  → 给 Agent 精准反馈，要求修复
  → 重新 verify

verify 失败第 2 次（相同问题）：
  ⚠️ 停止重试
  → 触发根因分析（Root Cause Analysis）
  → CEO 自问：
      1. 任务描述是否本来就不清楚？（输入问题）
      2. 角色选择是否有误？（配置问题）
      3. 产出标准是否不合理？（期望问题）
      4. 有没有我没考虑到的技术约束？（环境问题）
  → 根据根因，选择：修改任务描述/换角色/降低标准/拆分任务
  → 重新 spawn（不是重试）

verify 失败第 3 次：
  🛑 强制暂停
  → 把失败情况完整描述给用户
  → 请用户介入决策：降低标准？换方案？放弃这个产出？
  → 不再自主重试
```

### 根因分析模板

```
【verify 失败根因分析】
错误信息：{exact error}
失败次数：{N}

假设 1：{可能的原因}
验证方式：{怎么确认这个假设}
结论：{对/错}

假设 2：{可能的原因}
...

根因判断：{最可能的原因}
修复策略：{具体行动，不是"重试"}
```

### 为什么这样设计

- 连续失败 = 系统性问题，不是随机错误，重试没有意义
- 根因不找到，同样的失败会在其他项目中重现
- 第 3 次失败必须让人介入——人类的判断比 CEO 自主绕行更可靠

### 与 Phase 5 复盘的衔接

失败模式 → 记录到 `retrospective.failure_patterns` → `retro` 命令聚合分析 → 识别系统性问题
