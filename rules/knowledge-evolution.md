# Knowledge Evolution（知识进化机制）

> 借鉴 [makepad-skills](https://github.com/ZhangHanDong/makepad-skills) 的简化进化模式

---

## 核心流程

```
踩坑/学到新知识 → 知识识别四问 → 2+ YES → 直接写入 SKILL.md → 添加 Evolution Marker
```

---

## 知识识别四问

| 问题 | YES = 记录 | NO = 跳过 |
|------|-----------|-----------|
| **可复用？** | 其他项目也会遇到 | 仅此项目特有 |
| **费力？** | 调试 > 15 分钟 | 一眼看出 |
| **有帮助？** | 能预防未来问题 | 无预防价值 |
| **未文档化？** | 官方文档未提及 | 文档有说明 |

**判定**：2+ 个 YES = 记录到对应 SKILL.md

---

## Evolution Marker 格式

```markdown
<!-- Evolution: YYYY-MM-DD | source: {项目名} | trigger: {触发类型} | author: @{用户} -->
```

### 触发类型

| 类型 | 说明 |
|------|------|
| `pattern-extraction` | 从踩坑中提取的规则 |
| `version-adaptation` | 框架版本升级适配 |
| `self-correction` | 修正错误规则 |
| `personalization` | 个人偏好模式 |
| `description-improvement` | Skill 触发条件优化 |

---

## Description 进化规则

> **核心原则**：让 Skill 自己"举手"，而非硬编码触发。

### 何时更新 description

| 场景 | 行动 |
|------|------|
| Skill 应激活但未激活 | 添加漏掉的触发词到 description |
| 用户手动调用 Skill | 说明 description 不够清晰，需改进 |
| 发现新的使用场景 | 扩展 "Use when" 条件 |

### description 最佳格式

```yaml
description: |
  一句话说明 Skill 功能。
  Use when:
  - 具体场景 1
  - 具体场景 2
  - 具体场景 3
  触发词：关键词1、关键词2、关键词3
```

### 示例

```yaml
# 之前（模糊）
description: Zustand 状态管理最佳实践

# 之后（精确）
description: |
  Zustand 4.x 状态管理最佳实践。
  Use when:
  - 创建/修改 store、状态管理、全局状态
  - 文件路径包含 stores/、*Store.ts
  - 状态更新、订阅、中间件问题
  触发词：Zustand、store、状态、immer、shallow、useStore
```

---

## 写入位置

直接写入对应技术的 SKILL.md：

| 知识类型 | 目标文件 |
|---------|---------|
| Zustand 相关 | `~/.claude/skills/zustand-patterns/SKILL.md` |
| ReactFlow 相关 | `~/.claude/skills/reactflow-patterns/SKILL.md` |
| 其他技术 | 对应的 `skills/{tech}-patterns/SKILL.md` |

---

## 示例

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

## 废弃规则处理

不删除，标记为废弃：

```markdown
### 3.1 [DEPRECATED] 使用 memo 优化节点组件
<!-- Deprecated: 2026-01-10 | reason: React 19 自动优化 -->
```

---

**✅ 简化版进化机制** | **无中间层** | **git 天然支持回滚**
