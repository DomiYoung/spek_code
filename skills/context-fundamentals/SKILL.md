# Context Engineering 基础

> 上下文工程是管理 LLM 上下文窗口的学科。与提示工程不同，上下文工程关注的是进入模型有限注意力预算的所有信息的整体策划。

---

## 触发条件

Use when:
- 设计新 Agent 系统或修改现有架构
- 调试与上下文相关的意外行为
- 优化上下文使用以降低 token 成本
- 解释上下文窗口、注意力机制
- 讨论渐进式披露、上下文预算

触发词：understand context, explain context windows, design agent architecture, context budgeting, 上下文基础

---

## 核心概念

### 上下文的构成

| 组件 | 说明 | 特点 |
|------|------|------|
| **System Prompts** | Agent 的身份、约束、行为指南 | 会话开始加载，全程持久 |
| **Tool Definitions** | Agent 可执行的操作定义 | 位于上下文前端，影响行为导向 |
| **Retrieved Documents** | 领域知识、参考材料 | 按需加载（RAG） |
| **Message History** | 用户与 Agent 的对话历史 | 可能主导上下文使用 |
| **Tool Outputs** | 工具执行结果 | 可占总上下文 80%+ |

### 注意力预算约束

```
Token 数量增加 → 注意力被稀释 → 性能下降
```

**关键洞察**：
- 上下文窗口受限于**注意力机制**而非原始 token 容量
- 模型对短序列的训练更充分，长上下文精度降低
- "Lost-in-Middle" 现象：中间信息召回率下降 10-40%

### 渐进式披露原则

```
启动时 → 仅加载 Skill 名称 + 描述
激活时 → 加载完整 SKILL.md 内容
执行时 → 按需加载 references/
```

**优势**：保持 Agent 轻量，同时可按需访问更多上下文

---

## 实践指南

### 1. 信息质量 > 数量

```yaml
错误思维: 更大的上下文窗口 = 更好的性能
正确思维: 最小的高信号 token 集合 = 最优结果
```

**原则**：信息性 > 穷尽性

### 2. 注意力位置优化

```
┌─────────────────────────────────────┐
│  ★ 高注意力区：开头                  │
├─────────────────────────────────────┤
│  ⚠️ 低注意力区：中间（Lost-in-Middle）│
├─────────────────────────────────────┤
│  ★ 高注意力区：结尾                  │
└─────────────────────────────────────┘
```

**策略**：关键信息放在开头或结尾

### 3. System Prompt 组织

```markdown
<BACKGROUND_INFORMATION>
你是 Python 专家，帮助开发团队。
当前项目：Python 3.9+ 数据处理管道
</BACKGROUND_INFORMATION>

<INSTRUCTIONS>
- 编写干净、地道的 Python 代码
- 为函数签名添加类型提示
- 为公共函数添加 docstring
</INSTRUCTIONS>

<TOOL_GUIDANCE>
使用 bash 进行 shell 操作，python 进行代码任务。
文件操作使用 pathlib 以保持跨平台兼容。
</TOOL_GUIDANCE>

<OUTPUT_DESCRIPTION>
提供带语法高亮的代码块。
在注释中解释非显而易见的决策。
</OUTPUT_DESCRIPTION>
```

### 4. 文件系统作为外部存储

```yaml
# 不要一次加载所有文档
步骤 1: 加载摘要 → docs/api_summary.md
步骤 2: 按需加载 → docs/api/endpoints.md（仅当需要 API 调用时）
```

### 5. 上下文预算管理

| 阈值 | 行动 |
|------|------|
| < 70% | 正常运行 |
| 70-80% | 触发压缩策略 |
| > 80% | 强制压缩/分区 |

---

## 指导原则

1. **将上下文视为有限资源**，边际收益递减
2. **关键信息放在开头/结尾**，避免 Lost-in-Middle
3. **使用渐进式披露**，延迟加载直到需要
4. **用清晰的分节组织 System Prompt**
5. **开发期间监控上下文使用量**
6. **在 70-80% 利用率时触发压缩**
7. **为上下文退化设计**而非祈祷避免
8. **偏好小而高信号的上下文**而非大而低信号

---

## 关联技能

| 技能 | 关系 |
|------|------|
| `context-degradation` | 理解上下文如何失效 |
| `context-compression` | 压缩策略 |
| `context-optimization` | 扩展上下文容量的技术 |
| `multi-agent-patterns` | 上下文隔离如何支持多 Agent |

---

## 参考来源

- Agent Skills for Context Engineering (muratcankoylan)
- Transformer 注意力机制研究
- 领先 AI 实验室的生产工程指南

---

**Version**: 1.0.0 | **Created**: 2026-01-12 | **Author**: domiyoung
