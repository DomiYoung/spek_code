# Claude Code Behavioral Rules

Actionable rules for enhanced Claude Code framework operation.

> **📏 Size Governance**: This file must stay ≤200 lines. Verbose sections → `~/.claude/rules/`

---

## Rule Priority System

**🔴 CRITICAL**: Security, data safety, production breaks - Never compromise
**🟡 IMPORTANT**: Quality, maintainability, professionalism - Strong preference
**🟢 RECOMMENDED**: Optimization, style, best practices - Apply when practical

### Conflict Resolution
1. **Safety First**: Security/data rules always win
2. **Scope > Features**: Build only what's asked
3. **Quality > Speed**: Except in emergencies

---

## 🔴 Auto-Trigger Rules

### Task Weight Assessment
**Triggers**: 每个新任务开始时（无例外）

收到任务后必须**先输出权重评估**，决定 Spec-Kit/Task Master/专家路由 启用。

→ **详见**: `~/.claude/rules/task-weight.md`
→ **专家路由**: `~/.claude/skills/expert-router/SKILL.md`

### Pre-Implementation Checklist
**Triggers**: 任何代码编写前（Hook 强制）

编写代码前验证：需求明确、spec.md 存在、复用检查、权重评估、目录正确。

→ **详见**: `~/.claude/rules/pre-implementation.md`

### Skill Factory Protocol
**Triggers**: 创建 Skill、修改 knowledge

所有 Skill 必须包含 Trinity（红线+审计+自愈），Score ≥ 7 才入库。

→ **详见**: `~/.claude/rules/skill-factory.md`

### Completion Loop
**Triggers**: 任务完成、代码验证通过

验证通过 → 自动提交推送（lint + tsc + 无 console.log/any）

→ **详见**: `~/.claude/rules/completion-loop.md`

### Knowledge Value Assessment
**Triggers**: Bug 修复后、问题解决后、会话结束前

自动评估是否记录到 KI（满足 2+ 评估维度 → 记录）

→ **详见**: `~/.claude/rules/knowledge-assessment.md`

---

## Agent Orchestration
**Priority**: 🔴

- **Auto-Selection**: 根据关键词/文件类型自动选择专家
- **PM Agent**: 任务完成后自动记录模式/决策
- **Manual Override**: `@agent-[name]` 直接路由

---

## Workflow Rules
**Priority**: 🟡

- **Task Pattern**: Understand → Plan → TodoWrite(3+) → Execute → Validate
- **Batch Operations**: 默认并行，仅依赖时串行
- **Session Pattern**: SESSION.md load → Work → Checkpoint → Skills SKILL.md save

---

## Implementation Rules
**Priority**: 🟡

| Rule | Requirement |
|------|-------------|
| **Completeness** | Start = Finish, no TODO/Mock/Stub |
| **Scope** | Build ONLY what's asked, MVP first |
| **YAGNI** | No speculative features |

---

## Code Standards
**Priority**: 🟢

- Follow language conventions (camelCase/snake_case)
- Organize by feature/domain, not file type
- Clean temp files after operations, no artifact pollution

---

## Failure Investigation
**Priority**: 🔴

- **Root Cause Analysis**: Always investigate WHY
- **Never Skip**: Tests, validation, quality checks
- **Fix > Workaround**: Address underlying issues

---

## Professional Honesty
**Priority**: 🟡

- No marketing language ("blazingly fast", "100% secure")
- State "untested", "MVP", "needs validation" honestly

---

## Git Workflow
**Priority**: 🔴

- `git status && git branch` before starting
- Feature branches only, never main/master
- Incremental commits, verify before commit

---

## Tool Optimization
**Priority**: 🟢

| Task | Best Tool |
|------|-----------|
| Multi-file edits | MultiEdit |
| Complex analysis | Task agent |
| Code search | Grep tool |
| Documentation | Context7 MCP |

---

## Safety Rules
**Priority**: 🔴

- Check package.json/deps before using libraries
- Follow existing project conventions
- Plan → Execute → Verify for changes

---

## Temporal Awareness
**Priority**: 🔴

- Check `<env>` for "Today's date" before temporal assessment
- Never assume from knowledge cutoff

---

## Quick Reference

### 🔴 CRITICAL
- `git status && git branch` before starting
- Read before Write/Edit, Feature branches only
- Root cause analysis required

### 🟡 IMPORTANT
- TodoWrite for >3 step tasks
- Complete all started implementations, build only what's asked

### 🟢 RECOMMENDED
- Parallel over sequential, MCP tools over basic alternatives

---

## 📏 Meta-Rule: Size Governance

**This file must not exceed 200 lines.**

| 行为 | 判定 |
|------|------|
| 添加 ASCII 表格/流程图 | → 创建 `rules/*.md` |
| 添加 >10 行代码块 | → 创建 `rules/*.md` |
| 单个 section >20 行 | → 拆分到 `rules/*.md` |

---

## 📁 Modular Rules Index

| 规则文件 | 内容 |
|---------|------|
| `rules/task-weight.md` | 权重评估表格和决策规则 |
| `rules/pre-implementation.md` | 编码前检查清单和 Hook |
| `rules/skill-factory.md` | Skill 创建标准和质量门槛 |
| `rules/completion-loop.md` | 自动提交流程和验证 |
| `rules/knowledge-assessment.md` | 知识价值评估体系 |
