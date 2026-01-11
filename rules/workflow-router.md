# 工作流路由规则

> 统一的规划工作流选择：planning-with-files vs Spec-Kit

---

## 📊 路由决策表

```
┌─────────────────────────────────────────────────────────────────┐
│                    工作流路由决策                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  权重 ≥ 7?  ───YES──→  有 .specify/ 基础设施?                   │
│     │                        │                                  │
│     NO                      YES ──→ 🔵 Spec-Kit 流程            │
│     │                        │                                  │
│     ▼                       NO ──→ 初始化 .specify/ 或降级      │
│  权重 3-6?  ───YES──→  🟢 planning-with-files                   │
│     │                                                           │
│     NO                                                          │
│     │                                                           │
│     ▼                                                           │
│  权重 0-2   ────────→  ⚪ TodoWrite 即可                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 权重 → 工作流映射

| 权重 | 工作流 | 文件 | 说明 |
|------|--------|------|------|
| **≥ 7** | 🔵 Spec-Kit | `.specify/specs/{feature}/` | 新功能、重构、架构变更 |
| **5-6** | 🟢 planning-with-files | `.planning/` | 中型任务、多步骤实现 |
| **3-4** | 🟢 planning-with-files (轻量) | `.planning/` | 仅 task_plan.md |
| **0-2** | ⚪ TodoWrite | 无文件 | 简单任务，内存规划 |

---

## 🔵 Spec-Kit 流程（权重 ≥ 7）

**适用场景**：
- 新功能开发（用户故事、验收标准）
- 架构重构（影响 >5 文件）
- API/Schema 变更
- 需要团队协作的功能

**流程**：
```
/speckit.constitution  →  定义项目原则（一次性）
        ↓
/speckit.specify       →  创建功能规格 spec.md
        ↓
/speckit.clarify       →  澄清模糊需求（可选）
        ↓
/speckit.plan          →  技术方案 plan.md
        ↓
/speckit.tasks         →  任务拆解 tasks.md
        ↓
/speckit.analyze       →  一致性检查（可选）
        ↓
/speckit.implement     →  执行实现
```

**产出文件**：
```
.specify/
├── memory/
│   └── constitution.md      # 项目原则
└── specs/{feature}/
    ├── spec.md              # 功能规格
    ├── plan.md              # 技术方案
    └── tasks.md             # 任务清单
```

---

## 🟢 planning-with-files 流程（权重 3-6）

**适用场景**：
- 多步骤任务（>5 工具调用）
- 研究性任务
- 中等复杂度的 Bug 修复
- 需要持久化进度的任务

**流程**：
```
任务开始  →  创建 .planning/ 目录
    ↓
创建 task_plan.md    →  任务拆解、依赖关系
    ↓
执行任务  →  更新 progress.md（实时进度）
    ↓
记录发现  →  更新 findings.md（关键发现）
    ↓
任务完成  →  归档或删除 .planning/
```

**产出文件**：
```
.planning/
├── task_plan.md      # 任务计划（必需）
├── progress.md       # 执行进度（推荐）
└── findings.md       # 关键发现（可选）
```

**核心理念**：
```
Context Window = RAM (易失、有限)
Filesystem = Disk (持久、无限)
```

---

## ⚪ TodoWrite 流程（权重 0-2）

**适用场景**：
- 简单 Bug 修复（<3 文件）
- 文档更新
- 样式调整
- 代码分析/理解

**流程**：
```
任务开始  →  TodoWrite 创建任务列表
    ↓
执行任务  →  逐个标记完成
    ↓
任务完成  →  无持久化文件
```

---

## 🔄 降级规则

当 Spec-Kit 基础设施不存在时：

| 情况 | 处理 |
|------|------|
| 权重 ≥ 7 但无 `.specify/` | 询问用户：初始化 or 降级到 planning-with-files |
| 用户选择降级 | 使用 planning-with-files + 更详细的 task_plan.md |
| 用户选择初始化 | 执行 `specify init .` 或手动创建结构 |

---

## 📋 路由检查清单

每个任务开始时：

```markdown
## 工作流路由检查

1. 权重评估结果: __
2. 当前工作流: [Spec-Kit / planning-with-files / TodoWrite]
3. 基础设施检查:
   - [ ] .specify/ 存在（如需 Spec-Kit）
   - [ ] .planning/ 存在（如需 planning-with-files）
4. 路由决策: __
```

---

## 🔗 相关文件

- `rules/task-weight.md` - 权重评估详细规则
- `skills/planning-with-files/SKILL.md` - 文件规划技能
- `skills/speckit.*/SKILL.md` - Spec-Kit 系列技能
