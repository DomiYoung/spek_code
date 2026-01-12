---
description: ⚠️ DEPRECATED - 请使用 feature-dev skill 替代
---

# ⚠️ /sc 命令已废弃

**此命令已于 2026-01-09 废弃，请使用新的 `feature-dev` skill 系统替代。**

---

## 迁移指南

### 旧命令 → 新 Skill 映射

| 旧命令 | 新 Skill | 说明 |
|--------|----------|------|
| `/sc [task]` | `feature-dev:feature-dev` | 功能开发主入口 |
| `/sc frontend [task]` | `feature-dev:feature-dev` | 前端开发 |
| `/sc backend [task]` | `feature-dev:feature-dev` | 后端开发 |
| `/sc debug [task]` | `feature-dev:feature-dev` | 问题调试 |
| `/sc performance [task]` | `feature-dev:feature-dev` | 性能优化 |
| `/sc:troubleshoot` | `feature-dev:feature-dev` | 问题诊断 |
| `/sc:implement` | `feature-dev:feature-dev` | 功能实现 |
| `/sc:analyze` | `feature-dev:code-explorer` | 代码分析 |
| `/sc:design` | `feature-dev:code-architect` | 架构设计 |

### 新用法示例

```typescript
// 功能开发
Task({
  subagent_type: "feature-dev:feature-dev",
  prompt: "创建搜索组件"
});

// 代码分析
Task({
  subagent_type: "feature-dev:code-explorer",
  prompt: "分析 src/features/workflow 模块结构"
});

// 架构设计
Task({
  subagent_type: "feature-dev:code-architect",
  prompt: "设计用户权限管理系统"
});
```

### 可用的 feature-dev Agents

| Agent | 用途 |
|-------|------|
| `feature-dev:feature-dev` | 功能开发、Bug修复、优化 |
| `feature-dev:code-explorer` | 代码分析、架构理解 |
| `feature-dev:code-architect` | 架构设计、技术方案 |
| `feature-dev:code-reviewer` | 代码审查、质量检查 |

---

## 为什么废弃？

1. **统一入口**: `feature-dev` 提供更清晰的 agent 分工
2. **更好的上下文**: 专门化 agent 能更好地理解特定任务
3. **插件化架构**: 与 Claude 官方插件系统对齐

---

**迁移日期**: 2026-01-09
**替代方案**: `feature-dev` skill (claude-plugins-official)
