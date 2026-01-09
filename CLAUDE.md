# SuperClaude Entry Point

本文件是 SuperClaude 框架入口，采用模块化架构设计。

---

## 📁 目录结构（2026-01-08 重构）

```
~/.claude/
├── CLAUDE.md              # 本文件（入口）
├── core/                  # 核心框架文件
│   ├── RULES.md           # 行为规则
│   ├── PRINCIPLES.md      # 工程原则
│   ├── FLAGS.md           # 模式标志
│   ├── MODES.md           # 行为模式
│   ├── MCP_GUIDE.md       # MCP 服务器指南
│   ├── DECISION_TREES.md  # 决策树
│   └── TOOL_SELECTION.md  # 工具选择
├── skills/                # 技能库
│   ├── workflow/          # 工作流技能
│   │   └── workflow-orchestrator/
│   ├── experts/           # 专家技能
│   │   ├── frontend/      # 前端专家
│   │   ├── backend/       # 后端专家
│   │   ├── architect/     # 架构师
│   │   ├── product/       # 产品经理
│   │   ├── database/      # 数据库专家
│   │   ├── quality/       # 质量保障
│   │   └── domain/        # 领域专家 (dify, ragflow, okr...)
│   ├── patterns/          # 模式技能 (reactflow, zustand...)
│   └── tools/             # 工具技能 (xlsx, pdf...)
├── configs/               # 配置文件
│   └── triggers.yaml      # 自动触发规则
├── hooks/                 # 自动化钩子
├── templates/             # 格式模板（仅模板，不存数据）
├── rules/                 # 规则详情
└── backups/               # 归档备份
```

---

## 🔄 三层架构

| 层级 | 位置 | 职责 |
|------|------|------|
| **全局层** | `~/.claude/` | 框架、技能、配置 |
| **知识层** | `~/.ai-knowledge/` | 踩坑、决策、模式数据 |
| **项目层** | `{project}/` | 项目特定配置 |

---

## 📝 Git Commit 格式（全局强制）

**规则**：
1. **全中文**：标题和正文均使用中文（type/scope 除外）
2. **知识图谱格式**：核心改动、影响范围、技术背景、相关文件
3. **禁止敏感词**：严禁 AI/agent/claude/bot/GPT 等
4. **固定 Author**：`--author="YOUR_USERNAME <YOUR_USERNAME@gmail.com>"`

**格式**:
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
| `style` | 样式调整 |
| `docs` | 文档 |
| `chore` | 构建/依赖 |

---

## 🔐 需求冻结 Hook

**触发**：`.specify/specs/*/spec.md`、`PRD.md`、`requirements.md`

**豁免**：输入包含 `/skip-protect` 或 `跳过保护`

---

## ⚡ 自动触发规则

详见 `configs/triggers.yaml`，核心触发：

| 触发条件 | 动作 |
|---------|------|
| 任务开始 | 权重评估 → 路由到对应 Skill |
| 权重 ≥ 7 | 自动进入 Spec-Kit 流程 |
| 调试 > 15min | 提示记录到 pitfalls.md |
| 同一问题 2 次 | 自动记录踩坑 |
| Session 开始 | 读取 pitfalls + Serena memory |
| Session 结束 | 知识价值评估 + 保存进度 |

---

## 🎯 核心框架

@core/RULES.md
@core/PRINCIPLES.md
@core/FLAGS.md
@core/MODES.md
@core/MCP_GUIDE.md

---

## 📚 知识库位置

| 类型 | 位置 | 说明 |
|------|------|------|
| 全局踩坑 | `~/.ai-knowledge/global/pitfalls.md` | 跨项目通用 |
| 领域知识 | `~/.ai-knowledge/domains/{domain}/` | 技术领域特定 |
| 项目知识 | `~/.ai-knowledge/projects/{project}/` | 项目特定 |
| 模板 | `~/.claude/templates/` | 仅格式模板 |

---

**Last Updated**: 2026-01-08 | **Author**: YOUR_USERNAME
