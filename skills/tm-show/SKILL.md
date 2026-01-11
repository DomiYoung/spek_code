---
name: tm-show
description: |
  Task Master - 查看任务详情。
  Use when:
  - 查看指定任务详情
  - 了解任务上下文
  触发词：查看任务、任务详情、show task
  Related Skills: tm-next, tm-complete, speckit.tasks
globs:
  - ".taskmaster/**/*"
  - "**/tasks.md"
---

# Task Master: 查看任务详情

**查看指定任务的完整信息**: $ARGUMENTS

---

## 执行流程

### 1. 获取任务详情
```bash
mcp__task-master-ai__get_task --id="$ARGUMENTS" --projectRoot="$(pwd)"
```

### 2. 输出完整信息
```markdown
## 📋 任务详情

**任务 ID**: [ID]
**标题**: [title]
**描述**: [description]
**状态**: [status]
**优先级**: [priority]
**依赖**: [dependencies]
**创建时间**: [created]
**更新时间**: [updated]

### 🎯 实施细节
[details]

### 🧪 测试策略
[testStrategy]

### 📦 子任务列表
[subtasks with status]

### 🔗 依赖关系
[dependency graph if any]
```

---

## 🎯 使用示例

```bash
# 查看特定任务
/tm-show 1.2

# 查看主任务
/tm-show 1
```

---

**基于任务信息规划实施步骤**
