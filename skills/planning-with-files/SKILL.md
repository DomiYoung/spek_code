---
name: planning-with-files
description: |
  文件持久化规划工具 - 用于中等复杂度任务。
  Use when:
  - 任务权重 3-6 分（多文件变更但非架构级）
  - 需要 >5 次工具调用的多步骤任务
  - 研究性任务需要记录发现和进度
  - 任务可能跨 Session 需要持久化状态
  触发词：规划、计划、多步骤、复杂任务、进度跟踪、.planning
globs:
  - ".planning/**/*"
  - "**/task_plan.md"
  - "**/progress.md"
  - "**/findings.md"
---

# Planning with Files

**核心理念**：将规划和进度持久化到文件系统，避免上下文丢失

```
Context Window = RAM (易失、有限)
Filesystem = Disk (持久、无限)
```

---

## 触发条件

- 权重评估 3-6 分
- 任务需要 >5 次工具调用
- 多步骤任务需要持久化进度
- 研究性任务需要记录发现

---

## 目录结构

```
.planning/
├── task_plan.md      # 任务计划（必需）
├── progress.md       # 执行进度（推荐）
└── findings.md       # 关键发现（可选）
```

---

## 执行流程

### 1. 初始化规划目录

```bash
mkdir -p .planning
```

### 2. 创建 task_plan.md

```markdown
# Task Plan: [任务标题]

## 目标
[简述任务目标]

## 任务分解

- [ ] 1. [步骤1]
- [ ] 2. [步骤2]
- [ ] 3. [步骤3]

## 依赖关系
- 步骤2 依赖 步骤1
- 步骤3 依赖 步骤2

## 风险和注意事项
- [潜在风险]

## 完成标准
- [ ] [验收条件1]
- [ ] [验收条件2]
```

### 3. 执行时更新 progress.md

```markdown
# Progress Log

## [时间戳] 步骤1
- 状态: ✅ 完成 / 🔄 进行中 / ❌ 阻塞
- 产出: [文件/结果]
- 备注: [关键信息]

## [时间戳] 步骤2
- 状态: 🔄 进行中
- 当前进度: [描述]
```

### 4. 记录发现到 findings.md

```markdown
# Key Findings

## 发现1: [标题]
- 来源: [文件/调查]
- 影响: [对任务的影响]
- 行动: [需要采取的行动]

## 发现2: [标题]
...
```

### 5. 任务完成后

- 更新 task_plan.md 中所有任务为 ✅
- 决定是否保留 .planning/ 目录
- 有价值的发现迁移到项目文档

---

## 关键规则

### ✅ DO

1. **任务开始前**：先创建 task_plan.md
2. **每完成一步**：立即更新 progress.md
3. **发现问题**：记录到 findings.md
4. **上下文切换前**：确保进度已保存
5. **复杂决策**：写入文件而非仅在对话中说明

### ❌ DON'T

1. 不要仅依赖 TodoWrite（易失）
2. 不要在对话中隐藏错误（写入 findings.md）
3. 不要跳过进度更新
4. 不要在完成前删除 .planning/

---

## 读写决策矩阵

| 场景 | 操作 | 文件 |
|------|------|------|
| 任务开始 | WRITE | task_plan.md |
| 恢复任务 | READ | task_plan.md, progress.md |
| 完成步骤 | WRITE | progress.md |
| 发现问题 | WRITE | findings.md |
| 任务完成 | UPDATE | task_plan.md |

---

## 与其他工作流的关系

| 权重 | 工作流 | 说明 |
|------|--------|------|
| ≥ 7 | Spec-Kit | 使用 .specify/ 完整流程 |
| 3-6 | **planning-with-files** | 使用 .planning/ 轻量流程 |
| 0-2 | TodoWrite | 无持久化，内存规划 |

---

## 模板文件

参见：
- `templates/planning/task_plan.template.md`
- `templates/planning/progress.template.md`
- `templates/planning/findings.template.md`
