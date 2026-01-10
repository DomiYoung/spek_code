# Evolution Markers 规范

> 借鉴 [makepad-skills](https://github.com/ZhangHanDong/makepad-skills) 自进化机制
> 用于追踪 Skills 和知识的进化历史

---

## 概述

Evolution Markers 是一种嵌入在 Markdown 文件中的 HTML 注释标记，用于：

1. **追踪来源**：知道每条规则/知识从何而来
2. **支持回滚**：问题规则可快速定位和撤销
3. **个性化区分**：区分通用规则 vs 个人偏好
4. **进化观察**：观察 Skills 如何随时间进化

---

## 标记类型

### 1. Skill Evolution Marker

用于 `~/.claude/skills/*/SKILL.md` 中的规则变更：

```markdown
<!-- Evolution: YYYY-MM-DD | source: {项目名} | trigger: {触发类型} | author: @{用户} -->
```

**字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `YYYY-MM-DD` | 变更日期 | `2026-01-10` |
| `source` | 来源项目 | `react_ai`, `global` |
| `trigger` | 触发类型 | 见下方触发类型表 |
| `author` | 作者 | `@jinjia` |

**触发类型**：

| 类型 | 说明 |
|------|------|
| `version-adaptation` | 框架版本变化导致 |
| `pattern-extraction` | 从踩坑记录提取 |
| `self-correction` | 规则错误修正 |
| `personalization` | 个人偏好 |
| `usage-feedback` | 使用反馈优化 |
| `manual` | 手动添加 |

**示例**：

```markdown
### 2.5 反模式: Selector 返回新对象

**问题**: 每次返回新对象导致无限重渲染

```typescript
// ❌ 错误
const data = useStore(state => ({ a: state.a }));

// ✅ 正确
import { shallow } from 'zustand/shallow';
const data = useStore(state => ({ a: state.a }), shallow);
```

<!-- Evolution: 2026-01-10 | source: react_ai | trigger: pattern-extraction | author: @jinjia -->
```

---

### 2. KI (Knowledge Item) Marker

用于 `~/.ai-knowledge/*/pitfalls.md` 中的知识记录：

```markdown
<!-- KI: YYYY-MM-DD | score: {分数} | trigger: {触发类型} | project: {项目} -->
```

**字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `YYYY-MM-DD` | 记录日期 | `2026-01-10` |
| `score` | 知识价值评分 (1-10) | `5` |
| `trigger` | 触发类型 | 见下方触发类型表 |
| `project` | 来源项目 | `react_ai`, `global` |

**触发类型**：

| 类型 | 说明 |
|------|------|
| `bug-fix` | Bug 修复后记录 |
| `long-debug` | 长时间调试 (> 15min) |
| `repeated-error` | 重复错误 (2+ 次) |
| `user-request` | 用户主动记录 |
| `session-end` | 会话结束时记录 |

**示例**：

```markdown
### [2026-01-10] Zustand selector 导致无限重渲染

**现象**: 组件疯狂重渲染

**根因**: useStore 返回新对象，引用不稳定

**修复**: 使用 shallow 比较

<!-- KI: 2026-01-10 | score: 5 | trigger: long-debug | project: react_ai -->
```

---

### 3. Deprecated Marker

用于标记废弃的规则（不直接删除，保留历史）：

```markdown
<!-- Deprecated: YYYY-MM-DD | reason: {原因} -->
```

**示例**：

```markdown
### 3.1 [DEPRECATED] 使用 memo 优化节点组件

<!-- Deprecated: 2026-01-10 | reason: React 19 自动优化，不再需要手动 memo -->
```

---

## 使用指南

### 何时添加 Evolution Marker

| 场景 | 添加 |
|------|------|
| 新增规则 | ✅ 必须 |
| 修改规则 | ✅ 必须 |
| 废弃规则 | ✅ 使用 Deprecated Marker |
| 格式调整（无内容变化）| ❌ 不需要 |

### 何时添加 KI Marker

| 场景 | 添加 |
|------|------|
| 知识价值评分 ≥ 3 | ✅ 必须 |
| 知识价值评分 < 3 | ⚠️ 可选 |
| 敏感信息 | ❌ 禁止记录 |

### 标记位置

- **Skill Evolution Marker**: 放在被修改 section 的末尾
- **KI Marker**: 放在 pitfall 条目的末尾
- **Deprecated Marker**: 放在废弃 section 标题下方

---

## 工具支持

### 检索所有进化记录

```bash
# 检索所有 Evolution Markers
grep -r "<!-- Evolution:" ~/.claude/skills/ --include="*.md"

# 检索所有 KI Markers
grep -r "<!-- KI:" ~/.ai-knowledge/ --include="*.md"

# 检索所有废弃规则
grep -r "<!-- Deprecated:" ~/.claude/skills/ --include="*.md"
```

### 统计进化情况

```bash
# 统计本周进化次数
grep -r "<!-- Evolution:" ~/.claude/skills/ --include="*.md" | \
  grep "$(date +%Y-%m)" | wc -l

# 按触发类型统计
grep -r "<!-- Evolution:" ~/.claude/skills/ --include="*.md" | \
  grep -oP "trigger: \K[^|]+" | sort | uniq -c | sort -rn
```

---

## 与其他组件的关系

```
┌─────────────────────────────────────────────────────────────┐
│                     Evolution Markers                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ki-manager ──────────→ 添加 KI Marker                     │
│        │                                                     │
│        ▼                                                     │
│   skill-evolution-agent ──→ 添加 Evolution Marker           │
│                              添加 Deprecated Marker          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-10 | 初始版本，借鉴 makepad-skills |

---

**✅ Evolution Markers v1.0.0** | **makepad-skills 模式已集成**
