---
description: Task Master - 获取下一个可执行任务
---

# Task Master: 获取下一个任务

**获取当前可执行的下一个任务并显示详情**

---

## 执行流程

### 1. 获取下一个任务
```bash
mcp__task-master-ai__next_task --projectRoot="$(pwd)"
```

### 2. 如果返回任务ID，自动显示完整详情
```bash
mcp__task-master-ai__get_task --id="[返回的任务ID]" --projectRoot="$(pwd)"
```

### 3. 输出任务信息
```markdown
## 📋 下一个任务

**任务 ID**: [ID]
**标题**: [title]
**描述**: [description]
**状态**: [status]
**优先级**: [priority]
**依赖**: [dependencies]

### 实施细节
[details]

### 测试策略
[testStrategy]

### 子任务
[subtasks 列表]
```

### 4. 建议第一步行动
基于任务类型和复杂度：
- 简单任务（无子任务）→ 直接开始实现
- 有子任务 → 从第一个子任务开始
- 复杂度高 → 建议先使用 `/sc` 专家分析

---

## 🎯 使用示例

```bash
# 简单调用
/tm-next

# 如果没有任务
→ "✅ 所有任务已完成！"

# 如果有任务
→ 显示任务详情 + 建议第一步
```

---

**遵循三阶段流程执行任务**
