---
name: speckit.clarify
description: |
  需求澄清工具 - Spec-Kit 多轮对话式质量保障。
  Use when:
  - spec.md 有模糊/遗漏的地方
  - 需要向用户提问澄清需求
  - 任何创意工作、新功能设计前
  触发词：clarify、澄清、不清楚、确认需求
  Related Skills: speckit.specify, speckit.analyze, brainstorm
globs:
  - ".specify/**/*"
  - "**/spec.md"
---

# Speckit.Clarify（需求澄清）

> **Skill 类型**：Dialogue-driven（对话驱动型）
> **核心理念**：一次一问，选择题优先，渐进验证。

---

## Quick Start

```
加载 spec → 覆盖度扫描 → 多轮追问(5-8轮) → 分段确认设计 → 门控进入 Plan
```

---

## 核心流程（The Process）

### Phase 0: 加载与扫描

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` 获取：
   - `FEATURE_DIR`
   - `FEATURE_SPEC`

2. 加载 spec 文件，执行覆盖度扫描：

| 类别 | 状态 |
|------|------|
| Functional Scope & Behavior | Clear / Partial / Missing |
| Domain & Data Model | Clear / Partial / Missing |
| Interaction & UX Flow | Clear / Partial / Missing |
| Non-Functional Quality Attributes | Clear / Partial / Missing |
| Integration & External Dependencies | Clear / Partial / Missing |
| Edge Cases & Failure Handling | Clear / Partial / Missing |
| Constraints & Tradeoffs | Clear / Partial / Missing |
| Terminology & Consistency | Clear / Partial / Missing |
| Completion Signals | Clear / Partial / Missing |

3. 输出覆盖度卡片：

```
╔════════════════════════════════════════════════════════╗
║  📋 Spec 覆盖度扫描                                     ║
╠════════════════════════════════════════════════════════╣
║  ✅ Clear: [N] 项                                       ║
║  ⚠️ Partial: [N] 项                                     ║
║  ❌ Missing: [N] 项                                     ║
║  ──────────────────────────────────────────────────── ║
║  需澄清问题数: [N] 个（最多 8 个）                       ║
╚════════════════════════════════════════════════════════╝
```

### Phase 1: 多轮追问（5-8 轮）

**提问原则**：
- **一次一问** - 每条消息只包含一个问题
- **选择题优先** - 提供 2-4 个选项让用户选择
- **先给推荐** - 分析后给出推荐选项及理由
- **开放式补充** - 选择题无法覆盖时使用（限 ≤5 词回答）

**追问焦点**（按优先级）：
```
第 1-2 轮：核心功能边界 - "这个功能的范围是...？"
第 3-4 轮：数据模型 - "需要存储哪些关键数据？"
第 5-6 轮：交互流程 - "用户操作的主要路径是？"
第 7-8 轮：边缘情况 - "如果 X 失败，应该怎么处理？"
```

**问题格式**：

```markdown
### 问题 [N]/[总数]: [类别]

[问题描述]

**推荐**: 选项 [X] - [推荐理由]

| 选项 | 描述 | 适用场景 |
|------|------|----------|
| A | ... | ... |
| B | ... | ... |
| C | ... | ... |

请选择 (A/B/C) 或补充说明：
```

**每个回答后**：
1. 验证回答有效性
2. 立即更新 spec 文件的对应部分
3. 在 `## Clarifications` 下记录：`- Q: <问题> → A: <回答>`
4. 保存文件后再问下一个问题

### Phase 2: 分段确认设计

当关键问题澄清后（约 5 个问题后），进入分段确认：

**每段 200-300 字**，呈现澄清后的设计：
1. 功能范围确认
2. 数据模型确认
3. 交互流程确认
4. 边缘情况处理确认

**每段后必须确认**：
```
以上理解正确吗？有需要调整的地方吗？
```

### Phase 3: 门控进入 Plan

所有澄清完成后，**必须询问**：

```markdown
---
澄清已完成 ✓

**Spec 已更新**：[FEATURE_SPEC 路径]

**覆盖度变化**：
- Clear: [N] → [N+M]
- Partial: [N] → [N-X]
- Missing: [N] → [0]

**下一步选择**：
1. 📝 查看更新后的完整 Spec
2. 🚀 进入 `/speckit.plan` 生成实现计划
3. 🔄 还有其他需要澄清的地方

请选择 (1/2/3)：
```

**只有用户明确选择后才进入下一阶段**。

---

## 提问约束

| 约束 | 值 |
|------|-----|
| 单次会话最大问题数 | 8 |
| 选择题选项数 | 2-4 个 |
| 开放式回答长度 | ≤5 词 |
| 每个问题必须 | 影响架构/数据/测试/UX |

---

## 停止条件

以下情况停止追问：
- 所有 Missing/Partial 已解决
- 用户说 "done"、"够了"、"继续"
- 达到 8 个问题上限
- 用户选择跳过（需警告返工风险）

---

## 行为规则

1. **无歧义时** → "未检测到需要澄清的关键歧义。"
2. **缺少 spec 文件** → 提示先运行 `/speckit.specify`
3. **用户跳过** → 警告："跳过澄清会增加后续返工风险。确定继续？"
4. **每个回答后** → 立即写入 spec，不要批量更新

---

## 与 Brainstorm 的关系

| 场景 | 使用 Skill |
|------|-----------|
| 需求已有 spec.md，需要澄清细节 | **speckit.clarify** |
| 从零开始探索方案 | **brainstorm** |
| 澄清中发现需要方案对比 | clarify → 触发 brainstorm → 回到 clarify |

---

## Critical Guidelines

1. **一次一问** - 不要用多个问题轰炸用户
2. **选择题优先** - 比开放式问题更容易回答
3. **先给推荐** - 分析后明确推荐一个选项
4. **渐进验证** - 分段呈现，逐段确认
5. **门控 Plan** - 澄清确认前不进入 Plan 阶段
6. **即时保存** - 每个回答后立即更新 spec 文件
