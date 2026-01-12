---
name: 99-evolution
description: |
  Skills 自我进化机制 - 借鉴 makepad-skills 设计。
  Use when:
  - 会话结束时评估知识价值
  - 发现 Skill 需要更新
  - 新增踩坑经验
  触发词：进化、evolution、沉淀、记录踩坑
globs:
  - "skills/**/*.md"
---

# 99-evolution: Skills 自我进化机制

> 借鉴 [makepad-skills](https://github.com/ZhangHanDong/makepad-skills) 设计

---

## 核心机制

### 1. 知识四问评估

每次会话结束或问题解决后，评估是否需要沉淀知识：

| 问题 | 说明 |
|------|------|
| **可复用？** | 其他项目/场景可能遇到 |
| **费力？** | 花了 >15 分钟调试 |
| **有帮助？** | 能避免重复踩坑 |
| **未文档化？** | 官方文档没有说明 |

**2+ YES → 写入对应 `skills/{tech}-patterns/SKILL.md` + Evolution Marker**

---

### 2. Evolution Marker 格式

```markdown
<!-- Evolution: YYYY-MM-DD | source: {项目名} | trigger: {触发类型} | author: @{用户} -->
```

**触发类型**：
- `version-adaptation` - 框架版本变化
- `pattern-extraction` - 踩坑经验提取
- `self-correction` - 规则错误修正
- `personalization` - 个人偏好
- `usage-feedback` - 使用反馈优化

---

### 3. Self-Correction 机制

当 Skill 建议导致错误时：

1. 检测错误模式
2. 定位问题规则
3. 添加 Correction Marker
4. 更新规则内容

```markdown
<!-- Correction: YYYY-MM-DD | original: {原规则摘要} | fixed: {修正后摘要} -->
```

---

### 4. Deprecated Marker

废弃规则不删除，添加标记：

```markdown
<!-- Deprecated: YYYY-MM-DD | reason: {原因} -->
```

---

## 目录结构

```
skills/99-evolution/
├── SKILL.md           # 本文件（机制说明）
├── _base/             # 官方/通用模式（不修改）
├── community/         # 个人/社区贡献
├── templates/         # 模板文件
│   ├── pattern.md     # 模式模板
│   ├── pitfall.md     # 踩坑模板
│   └── troubleshoot.md # 问题排查模板
└── hooks/             # 自动化脚本
    ├── session-end.sh # 会话结束时提示
    └── post-error.sh  # 错误后捕获
```

---

## 写入流程

```
发现有价值知识
      │
      ▼
┌─────────────────────────┐
│  知识四问评估            │
│  ├── 可复用？           │
│  ├── 费力？             │
│  ├── 有帮助？           │
│  └── 未文档化？         │
└───────────┬─────────────┘
            │
      2+ YES?
            │
    ┌───────┴───────┐
    ▼               ▼
   YES              NO
    │               │
    ▼               ▼
写入 SKILL.md      跳过
+ Evolution Marker
```

---

## 检索命令

```bash
# 查看所有进化记录
grep -r "<!-- Evolution:" ~/.claude/skills/ --include="*.md"

# 查看所有修正记录
grep -r "<!-- Correction:" ~/.claude/skills/ --include="*.md"

# 查看所有废弃规则
grep -r "<!-- Deprecated:" ~/.claude/skills/ --include="*.md"

# 按触发类型统计
grep -r "<!-- Evolution:" ~/.claude/skills/ --include="*.md" | \
  grep -oP "trigger: \K[^|]+" | sort | uniq -c | sort -rn
```

---

## 与其他组件关系

| 组件 | 关系 |
|------|------|
| `workflow-orchestrator` | 任务完成后触发知识评估 |
| `skills/{tech}-patterns` | 知识写入目标 |
| `templates/evolution-markers.md` | Marker 格式规范 |

---

**Version**: 1.0.0 | **Last Updated**: 2026-01-12
