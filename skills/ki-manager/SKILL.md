---
name: ki-manager
description: "Knowledge Iteration 管理专家。负责会话结束前的经验沉淀、KI更新、Skills优化。触发：用户说'总结一下'、'记录经验'、'沉淀知识'、'会话结束'、功能完成、Superpowers finishing阶段。自动反思并更新KI文件。"
---

# KI Manager - Knowledge Iteration 管理专家

> **核心职责**: 在每次会话结束前，主动反思并沉淀经验到 KI 系统。

## KI 系统位置

```
~/.gemini/antigravity/knowledge/contentrss/artifacts/
├── product/
│   └── feature_decisions.md       # 功能决策记录
├── technical/
│   ├── pitfalls.md                # 踩坑记录
│   ├── architecture_decisions.md  # 架构决策 (ADR)
│   └── component_patterns.md      # 组件设计模式
├── ui/
│   └── design_system.md           # 设计系统规范
└── strategy/
    └── project_goals.md           # 项目目标和策略
```

---

## 触发条件

### 自动触发
- Superpowers **finishing** 阶段完成后
- 用户说 "总结一下"、"记录经验"、"沉淀知识"
- 完成一个功能开发后

### 手动触发
- 用户显式调用: `/skill ki-manager`

---

## 反思清单（5项检查）

### 1. 踩坑经验检查 🕳️

**问题**:
- 本次开发是否遇到意外的技术问题？
- 是否有调试很久才解决的 bug？
- 是否有文档不清晰导致的误用？

**行动**: 如果有，记录到 `technical/pitfalls.md`

**格式**:
```markdown
### ❌ 坑 X: [简短描述]
**日期**: YYYY-MM-DD
**问题**: [详细问题描述]
**解决**: [解决方案]
**教训**: [一句话经验]
```

---

### 2. 架构决策检查 🏗️

**问题**:
- 本次开发是否做了重要的技术选型？
- 是否选择了某个库/框架/工具？
- 是否有架构层面的变更？

**行动**: 如果有，记录到 `technical/architecture_decisions.md`

**格式**:
```markdown
## ADR-XXX: [决策标题]

**日期**: YYYY-MM-DD
**状态**: ✅ 已采纳 / ⚠️ 讨论中 / ❌ 已废弃

**背景**: [为什么需要这个决策]
**决策**: [具体决策内容]
**理由**: [决策理由]
**后果**: [采纳后的影响]
```

---

### 3. 组件模式检查 🧩

**问题**:
- 本次开发是否创建了可复用的组件？
- 是否发现了更优的组件设计模式？
- 是否有值得推广的代码模式？

**行动**: 如果有，记录到 `technical/component_patterns.md`

**格式**:
```markdown
### [模式名称]

**规则**: [一句话规则]

**示例**:
\`\`\`tsx
// ✅ 正确
[示例代码]

// ❌ 错误
[反例代码]
\`\`\`

**原因**: [为什么这样做]
```

---

### 4. 功能决策检查 📋

**问题**:
- 本次开发是否做了重要的功能决策？
- 是否有功能被废弃或调整？
- 是否有用户反馈影响了功能设计？

**行动**: 如果有，记录到 `product/feature_decisions.md`

---

### 5. Skills 优化检查 ⚡

**问题**:
- 某个 Skill 的触发词是否不够准确？
- 某个 Skill 的逻辑是否需要优化？
- 是否需要创建新的 Skill？

**行动**: 如果有，更新相应 Skill 的 `SKILL.md`

---

## 工作流

### Step 1: 反思本次会话
```yaml
回顾:
  - 完成了什么功能？
  - 遇到了什么问题？
  - 做了什么决策？
  - 发现了什么模式？
```

### Step 2: 逐项检查反思清单
```yaml
依次检查:
  1. 踩坑经验
  2. 架构决策
  3. 组件模式
  4. 功能决策
  5. Skills 优化
```

### Step 3: 更新 KI 文件
```yaml
操作:
  1. Read 相应 KI 文件
  2. 使用 Edit 工具追加新内容
  3. 保持格式一致性
```

### Step 4: 输出摘要
```yaml
输出:
  ✅ 已记录 X 条踩坑经验
  ✅ 已记录 Y 个架构决策
  ✅ 已更新 Z 个组件模式
```

---

## 输出示例

```
📝 KI 反思完成

本次会话沉淀:

### 踩坑经验 (1条)
- ❌ 坑 6: user_follows 表忘记添加唯一索引导致重复关注
  → 已记录到 pitfalls.md

### 架构决策 (1个)
- ADR-004: 选择双向关注而非单向关注
  → 已记录到 architecture_decisions.md

### 组件模式 (1个)
- FollowButton 乐观更新模式
  → 已记录到 component_patterns.md

---
✅ 下次开发类似功能时将自动避免这些坑
```

---

## 与其他 Skills 的协作

| Skill | 协作方式 |
|:---|:---|
| **Superpowers finishing** | finishing 完成后自动触发 ki-manager |
| **component-reuse-expert** | 新建的组件记录到 component_patterns.md |
| **product-manager** | 功能决策记录到 feature_decisions.md |

---

## KI 读取（会话启动时）

> **新会话启动时，应先读取 KI 以避免重复踩坑**

推荐读取顺序:
1. `technical/pitfalls.md` - 避免已知坑
2. `technical/component_patterns.md` - 复用已验证模式
3. `product/feature_decisions.md` - 了解产品方向

---

## 价值说明

| 没有 KI | 有 KI |
|:---|:---|
| 每次都可能重新踩坑 | 自动避免已知坑 |
| 忘记为什么这样设计 | 有 ADR 记录可查 |
| 每次都要重新思考模式 | 直接使用已验证模式 |
| Skills 永远不进化 | 持续优化，越用越好 |
