# SuperClaude Entry Point

本文件是 SuperClaude 框架入口，采用模块化架构设计。

---

## 🚨 Session 协议（每次会话必读）

### Session 开始时自动执行

```
1. claude-mem 自动注入上下文（Hooks 自动）
2. 检查 Task Master → mcp__task-master-ai__next_task()
3. 检查项目 SESSION.md → 恢复上次进度
```

### 任务开始时自动执行

```
1. 权重评估（必须输出决策卡片）
   ├── 噪音过滤：格式化/依赖更新/文档修正 → 直接 TodoWrite
   ├── 硬门槛检测：Breaking Change/鉴权/支付/跨服务 → Spec-Kit
   └── 打分路由：≥7 Spec-Kit / 3-6 planning-with-files / 1-2 TodoWrite

2. 工作流自动启动（不等用户确认）
   ├── Spec-Kit → 读取 skills/speckit.constitution/SKILL.md 开始执行
   ├── planning-with-files → 创建 .planning/task_plan.md
   └── TodoWrite → 直接创建任务列表开始工作
```

### Session 结束时自动执行

```
1. 知识价值评估（四问：可复用？费力？有帮助？未文档化？）
   └── 2+ YES → 写入对应 SKILL.md + Evolution Marker

2. claude-mem 自动保存会话摘要（Hooks 自动）

3. 更新 SESSION.md 进度
```

---

## 📁 目录结构

```
~/.claude/
├── CLAUDE.md              # 本文件（入口 + 协议）
├── core/                  # 核心框架
│   ├── RULES.md           # 行为规则
│   ├── PRINCIPLES.md      # 工程原则
│   ├── FLAGS.md           # 模式标志
│   ├── MODES.md           # 行为模式
│   └── MCP_GUIDE.md       # MCP 服务器指南
├── skills/                # 技能库（65+）
│   ├── speckit.*/         # Spec-Kit 系列（9个）
│   ├── planning-with-files/ # 轻量规划
│   ├── mem-*/             # 记忆系统（2个）
│   ├── experts/           # 专家技能（7个）
│   ├── patterns/          # 模式技能（18个）
│   └── tools/             # 工具技能
├── configs/               # 配置文件
│   └── workflow-rules.yaml # 工作流路由规则
├── rules/                 # 规则详情
│   ├── task-weight.md     # 权重评估
│   ├── workflow-router.md # 工作流路由
│   └── knowledge-evolution.md # 知识进化
├── hooks/                 # 自动化钩子
└── templates/             # 格式模板
```

---

## 🔄 两层架构

| 层级 | 位置 | 职责 |
|------|------|------|
| **全局层** | `~/.claude/` | 框架、技能、配置 |
| **项目层** | `{project}/` | 项目特定配置 |

---

## ⚡ 工作流路由（每个任务必须输出决策卡片）

### 🔴 强制：决策卡片输出格式

**每个任务开始时必须输出以下卡片，不可跳过：**

```
╔════════════════════════════════════════════════════════╗
║  📊 任务权重分析                                        ║
╠════════════════════════════════════════════════════════╣
║  任务描述: [一句话描述]                                  ║
╠──────────────────────────────────┬────────┬────────────╣
║  触发条件                        │  权重  │  命中       ║
╠──────────────────────────────────┼────────┼────────────╣
║  Breaking Change / Schema 迁移   │  强制  │  [ ]       ║
║  鉴权/支付/审计/跨服务            │  强制  │  [ ]       ║
║  新功能 / 重构                   │  +10   │  [ ]       ║
║  >5 文件 或 >200 行              │  +8    │  [ ]       ║
║  API/架构 变更                   │  +7    │  [ ]       ║
║  3-5 文件功能变更                │  +5    │  [ ]       ║
║  简单 Bug（<3 文件）             │  +2    │  [ ]       ║
║  纯样式/文档/格式化              │  +1    │  [ ]       ║
╠──────────────────────────────────┴────────┴────────────╣
║  📈 总权重: [X]                                         ║
║  🎯 工作流: [Spec-Kit / planning-with-files / TodoWrite]║
║  🧠 思考深度: [think / think-hard / ultrathink]         ║
╚════════════════════════════════════════════════════════╝
```

### Stage A: 硬门槛（直接判定，不看分数）

| 条件 | 路由 |
|------|------|
| 格式化/依赖更新/文档修正/重命名 | → TodoWrite（跳过评估） |
| Breaking Change / Schema 迁移 | → Spec-Kit（强制升级） |
| 鉴权/支付/审计 | → Spec-Kit（强制升级） |
| 跨服务调用链 | → Spec-Kit（强制升级） |

### Stage B: 打分路由（Stage A 未命中时）

| 维度 | 低(1-2) | 中(3-4) | 高(5+) |
|------|---------|---------|--------|
| 文件数 | 1-2 | 3-5 | 6+ |
| 模块跨度 | 单模块 | 2模块 | 3+模块 |
| API变更 | 无 | 内部 | 公开 |
| 测试复杂度 | 手动验证 | 单元测试 | E2E测试 |

**路由规则**: `总分 = max(复杂度, 风险)`
- ≥7 → Spec-Kit（读取 `skills/speckit.constitution/SKILL.md`）
- 5-6 → planning-with-files（创建 `.planning/task_plan.md`）
- 3-4 → planning-with-files-lite（仅 task_plan.md）
- 1-2 → TodoWrite（直接执行）

### 豁免条件

用户明确说「跳过评估」「直接开始」时可跳过决策卡片。

---

## 📝 Git Commit 格式（全局强制）

```
<type>(<scope>): <用户价值描述（中文）>

核心改动：<关键变更点>
影响范围：<涉及模块>
技术背景：<为什么这样做>
相关文件：<文件统计>
```

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `docs` | 文档 |
| `chore` | 构建/依赖 |

**Author**: `--author="domiyoung <domiyoung@gmail.com>"`

---

## 🔐 保护规则

| 触发文件 | 行为 |
|---------|------|
| `.specify/specs/*/spec.md` | 修改前确认 |
| `PRD.md` / `requirements.md` | 修改前确认 |

**豁免**: 输入包含 `/skip-protect` 或 `跳过保护`

---

## 🧠 两套记忆系统

| 系统 | 用途 | 触发方式 |
|------|------|---------|
| **claude-mem** | 工具调用历史、会话上下文 | Hooks 自动（无需干预） |
| **Skills SKILL.md** | 踩坑经验 + Evolution Marker | 知识四问 → 2+ YES → 写入 |

> **知识写入位置**: 按技术分类写入 `skills/{tech}-patterns/SKILL.md`

---

## 🎯 核心框架引用

@core/RULES.md
@core/PRINCIPLES.md
@core/FLAGS.md
@core/MODES.md
@core/MCP_GUIDE.md

---

## 🔌 Skill 自动激活机制

> **核心原则**: Skills 通过 description 语义匹配自动激活，无需硬编码触发。

### 激活流程

```
用户输入
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Claude 读取所有 Skills 的 name + description           │
│  └── 语义匹配：根据 description 判断是否适用            │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  匹配成功 → 自动读取 skills/[skill-name]/SKILL.md       │
│  └── 按 SKILL.md 指导执行任务                           │
└─────────────────────────────────────────────────────────┘
```

### description 最佳格式

```yaml
description: |
  一句话说明 Skill 功能。
  Use when:
  - 具体场景 1
  - 具体场景 2
  触发词：关键词1、关键词2
```

### 1% 原则

> **如果有 1% 的可能性某个 Skill 适用，必须调用它。**

### Skill 进化机制

Session 结束时自动检测：
- Skill 应激活但未激活 → 更新 description 添加触发词
- 用户手动调用 Skill → description 不够清晰，需改进
- 学到新知识 → 知识四问 → 2+ YES → 写入 SKILL.md + Evolution Marker

详见 `rules/knowledge-evolution.md`

---

**Last Updated**: 2026-01-11 | **Author**: domiyoung
