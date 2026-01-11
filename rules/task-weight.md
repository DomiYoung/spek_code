# Task Weight Assessment

> 详细权重评估表格，由 RULES.md 引用

## 权重评估表格

```
┌─ 权重评估 ────────────────────────────────────┐
│ □ 新功能/重构/Breaking Change?    → +10      │
│ □ >5 文件 或 >200 行?             → +8       │
│ □ API/架构/Schema 变更?           → +7       │
│ □ 3-5 文件功能变更?               → +5       │
│ □ 简单 Bug (<3 文件)?             → +2       │
│ □ 纯样式/文档?                    → +1       │
│ □ 代码分析/理解（非实现）?        → +0       │
│───────────────────────────────────────────────│
│ 总权重: __                                    │
│ → 工作流: [Spec-Kit(≥7) / planning-with-files(3-6) / TodoWrite(0-2)] │
│ → Task Master: [是(>3步)/否]                 │
│ → 专家路由: [专家名/无] → expert-router     │
│ → 模式: [--think/--research/默认]            │
└───────────────────────────────────────────────┘
```

## 工作流路由规则

| 权重 | 工作流 | 目录 | 说明 |
|------|--------|------|------|
| ≥ 7 | 🔵 Spec-Kit | `.specify/specs/{feature}/` | 完整规格流程 |
| 5-6 | 🟢 planning-with-files | `.planning/` | 文件持久化规划 |
| 3-4 | 🟢 planning-with-files (轻量) | `.planning/` | 仅 task_plan.md |
| 0-2 | ⚪ TodoWrite | 无 | 内存规划 |

## 工作流详情

### 🔵 Spec-Kit (权重 ≥ 7)

**触发**: 新功能、重构、架构变更、>5 文件

**流程**: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`

**产出**: `spec.md`, `plan.md`, `tasks.md`

### 🟢 planning-with-files (权重 3-6)

**触发**: 多步骤任务、>5 工具调用、需要持久化进度

**流程**: 创建 `.planning/` → `task_plan.md` → 执行 → `progress.md`

**产出**: `task_plan.md`, `progress.md`, `findings.md`

### ⚪ TodoWrite (权重 0-2)

**触发**: 简单 Bug、文档、样式、分析任务

**流程**: TodoWrite 创建任务 → 执行 → 标记完成

**产出**: 无持久化文件

## 降级规则

当 `.specify/` 不存在但权重 ≥ 7 时：
1. 询问用户：初始化 Spec-Kit 还是降级？
2. 降级：使用 planning-with-files + 详细 task_plan.md

## 豁免场景

- 用户明确说"跳过评估"、"直接开始"
- 纯问答对话（非任务执行）

## 决策树参考

详见 `DECISION_TREES.md` 的三棵决策树：
1. **复杂度决策树** → Spec-Kit/Task Master 启用
2. **专家路由决策树** → expert-router Skill
3. **模式标志决策树** → --think/--research 等标志
