---
description: Task Master - 完成任务并自动获取下一个
---

# Task Master: 完成任务

**完成任务**: $ARGUMENTS

---

## 执行流程

### 1. 验证任务完成度
检查任务是否真正完成：
- ✅ 所有代码已提交
- ✅ 测试通过
- ✅ 文档已更新
- ✅ PR已合并（如适用）

### 2. 标记任务为完成
```bash
mcp__task-master-ai__set_task_status \
  --id="$ARGUMENTS" \
  --status="done" \
  --projectRoot="$(pwd)"
```

### 3. 更新任务日志
```bash
mcp__task-master-ai__update_task \
  --id="$ARGUMENTS" \
  --prompt="[$(date)] 任务已完成并验证" \
  --projectRoot="$(pwd)"
```

### 4. 自动获取下一个任务
```bash
mcp__task-master-ai__next_task --projectRoot="$(pwd)"
```

### 5. 输出完成信息
```markdown
## ✅ 任务已完成

**完成任务**: [ID] - [title]
**完成时间**: [timestamp]

## 📋 下一个任务

[下一个任务信息 或 "所有任务已完成！"]
```

---

## 🎯 使用示例

```bash
# 完成当前任务
/tm-complete 1.2

# 完成主任务
/tm-complete 1
```

---

## ⚠️ 重要提醒

只有在以下情况下才标记为完成：
1. 代码已全部实现并测试通过
2. 相关文档已更新
3. PR已提交/合并（如适用）
4. 无遗留问题或技术债务

**未完全完成时请使用其他状态**：
- `in-progress` - 正在进行中
- `review` - 等待审查
- `blocked` - 被阻塞
