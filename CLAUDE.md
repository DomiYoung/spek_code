# SuperClaude 项目配置

> 精简版，减少上下文开销。

---

## 权重评估（每个任务必须）

| 条件 | 路由 |
|------|------|
| Breaking Change / 鉴权 / 支付 | → Spec-Kit |
| ≥7 分（多文件/跨模块） | → Spec-Kit |
| 3-6 分 | → planning-with-files |
| 1-2 分 | → TodoWrite |

---

## Superpowers 自动工作流 (必须遵循)

<EXTREMELY-IMPORTANT>
以下工作流自动触发，不需要手动调用。检测到关键词时自动启用对应 Skill。
</EXTREMELY-IMPORTANT>

### 触发流程

```
用户请求 → 检测意图 → 自动路由
    ↓
┌─────────────────────────────────────────────────────────┐
│ 1. 创建/设计任务 → 🧠 brainstorming-sp                    │
│    关键词: 创建、开发、设计、新功能、组件、feature          │
├─────────────────────────────────────────────────────────┤
│ 2. 设计完成后 → 📋 writing-plans-sp                       │
│    关键词: 计划、规划、怎么做、步骤                         │
├─────────────────────────────────────────────────────────┤
│ 3. 计划完成后 → 🚀 subagent-driven-development            │
│    关键词: 执行、开始、实现、go                            │
├─────────────────────────────────────────────────────────┤
│ 4. 编码过程中 → 🧪 test-driven-development (强制)         │
│    规则: 先写测试，再写代码，红绿重构                       │
├─────────────────────────────────────────────────────────┤
│ 5. 遇到问题时 → 🔍 systematic-debugging                   │
│    关键词: bug、错误、失败、不工作、调试                    │
├─────────────────────────────────────────────────────────┤
│ 6. 完成前 → ✅ verification-before-completion             │
│    规则: 提交前必须验证                                    │
└─────────────────────────────────────────────────────────┘
```

### 强制规则

- **TDD 不可跳过**: 所有代码必须先写测试
- **验证不可跳过**: 完成前必须运行验证
- **Brainstorming 优先**: 创建任务必须先构思设计

---

## Deep Research 自动触发

关键词触发: 研究、调研、分析、深度搜索、技术选型、竞品分析

```
/deep-research [topic]  # 手动触发
自动检测研究意图 → 🔬 deep-research skill
```

---

## Git Commit

```
<type>(<scope>): <用户价值（中文）>

核心改动：<变更点>
影响范围：<模块>
```

**Author**: `--author="domiyoung <domiyoung@gmail.com>"`

---

## Skills 索引

| 分类 | Skills |
|------|--------|
| **编排** | workflow-orchestrator |
| **规划** | planning-with-files, spec-first-development |
| **Superpowers** | brainstorming-sp, writing-plans-sp, subagent-driven-development, test-driven-development, systematic-debugging, verification-before-completion |
| **研究** | deep-research, got-controller, citation-validator |
| **专家** | frontend-expert, backend-expert, architect |
| **模式** | reactflow-patterns, zustand-patterns |

---

## 1% 原则

> **如果有 1% 的可能性某个 Skill 适用，必须调用它。**

---

**Last Updated**: 2026-01-13
