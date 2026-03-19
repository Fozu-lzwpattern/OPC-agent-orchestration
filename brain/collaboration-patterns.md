# 协作模式

## 模式1：串行流水线

```
A → B → C
```

- 适用：严格依赖顺序
- 示例：策划 → 搭建 → 发布
- 实现：A 完成后 spawn B，B 完成后 spawn C

## 模式2：并行分工

```
    ┌─ B1 ─┐
A ──┼─ B2 ─┼── C
    └─ B3 ─┘
```

- 适用：独立子任务可同时进行
- 示例：搭建员/内容员/供给员 同时工作
- 实现：A 完成后同时 spawn B1/B2/B3，全部完成后 spawn C
- 注意：需要追踪所有并行任务状态

## 模式3：迭代反馈

```
A ←→ B → C
```

- 适用：需要审核/修改循环
- 示例：搭建员 ↔ QA审核员 → 发布员
- 实现：A 完成后 spawn B，B 不通过则 sessions_send 给 A 修改

## 模式4：分治汇总

```
    ┌─ A1 ─┐
任务─┼─ A2 ─┼── 汇总
    └─ A3 ─┘
```

- 适用：大任务可拆分为独立子任务
- 示例：3 个研究员分别研究，最后文档员汇总
- 实现：同时 spawn A1/A2/A3，全部完成后 spawn 汇总员

## 模式选择决策

| 场景 | 推荐模式 |
|------|---------|
| 任务有严格先后顺序 | 串行 |
| 多个独立子任务 | 并行 |
| 产出需要质量审核 | 迭代 |
| 大任务可拆分 | 分治 |
| 复杂项目 | 混合（串行+并行+迭代）|

## 混合示例：营销活动

```
策划 ──→ 预算 ──→ ┬── 搭建 ──┬──→ QA ←→ 搭建 ──→ 发布
                   ├── 内容 ──┤
                   └── 供给 ──┘
```

阶段1：串行（策划→预算）
阶段2：并行（搭建/内容/供给）
阶段3：迭代（QA↔搭建）
阶段4：串行（发布）


---

## task-graph 使用指南（v5.1）

在 Phase 1（规划阶段）完成任务拆解后，CEO 应立即声明依赖图：

```bash
# 示例：研究项目，两个研究员并行，汇总员串行
python3 engine/project_state.py task-graph <pid> add researcher_a "" reports/topic-a.md
python3 engine/project_state.py task-graph <pid> add researcher_b "" reports/topic-b.md
python3 engine/project_state.py task-graph <pid> add integrator "researcher_a,researcher_b" reports/final.md

# 查看并行组（spawn 决策依据）
python3 engine/project_state.py task-graph <pid> show
# 输出：可并行启动: ['researcher_a', 'researcher_b']
```

**执行策略**：

```
task-graph show → 找出"可并行启动"列表
    │
    ├── 并行组：同时 spawn，监控各自完成
    │   └── 全部完成 → verify 各自产出 → 启动下游
    └── 串行节点：等依赖项全部完成后再 spawn
```

**context compaction 后恢复**：

```bash
python3 engine/project_state.py restore <pid>
# restore 会输出 task_graph，CEO 根据已完成节点判断从哪里继续
```
