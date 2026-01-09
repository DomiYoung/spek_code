---
name: task-classifier
description: "任务分类专家。在用户提出任何请求时自动分类：(1) 类型分类：Feature/Bug/Improvement (2) 领域分类：UI/Logic/Data/Infra (3) 根据分类选择不同工作流。触发：任何任务开始前自动执行。确保不同类型任务使用正确的处理流程。"
---

# Task Classifier Expert

> **核心理念**：先分类，后执行。不同类型的任务需要不同的工作流。

## 触发条件

**始终自动触发**：在处理任何用户请求前，先进行任务分类。

## 分类维度

### 维度 1：任务类型

| 类型 | 特征关键词 | 工作流 |
|:---|:---|:---|
| **Feature (新需求)** | "我想做"、"新增"、"添加功能"、"实现" | brainstorming → spec-first → 完整开发 |
| **Bug (问题修复)** | "报错"、"不工作"、"崩溃"、"修复"、"bug" | 复现 → 定位 → 修复 → 验证 |
| **Improvement (优化)** | "优化"、"改进"、"重构"、"性能" | 分析 → 方案 → 实施 → 对比 |
| **Question (咨询)** | "怎么"、"为什么"、"是什么" | 直接回答，无需工作流 |

### 维度 2：问题领域

| 领域 | 特征关键词 | 主要 Skills |
|:---|:---|:---|
| **UI (界面)** | "样式"、"布局"、"动画"、"颜色"、"响应式" | frontend-design, framer-motion-expert, tailwindcss-expert |
| **Logic (逻辑)** | "API"、"接口"、"数据处理"、"算法" | backend-expert, flask-expert, react-expert |
| **Data (数据)** | "数据库"、"表"、"查询"、"存储" | database-expert |
| **Infra (基础设施)** | "部署"、"配置"、"环境"、"CI/CD" | (需要时创建) |

## 分类矩阵

```
                    UI          Logic        Data         Infra
              ┌──────────┬──────────┬──────────┬──────────┐
  Feature     │ UI设计   │ 功能开发 │ 模型设计 │ 架构设计 │
              │ 需求流程 │ 需求流程 │ 需求流程 │ 需求流程 │
              ├──────────┼──────────┼──────────┼──────────┤
  Bug         │ 样式修复 │ 逻辑修复 │ 数据修复 │ 配置修复 │
              │ 快速修复 │ 调试流程 │ 调试流程 │ 快速修复 │
              ├──────────┼──────────┼──────────┼──────────┤
  Improvement │ UI优化   │ 代码重构 │ 性能优化 │ 架构优化 │
              │ 设计评审 │ 代码评审 │ 分析优化 │ 架构评审 │
              └──────────┴──────────┴──────────┴──────────┘
```

## 工作流差异

### Feature 工作流（完整流程）
```
1. component-reuse-expert → 检查复用
2. brainstorming → 需求澄清
3. spec-first-development → 创建规范
4. [执行层 Skills] → 开发实现
5. webapp-testing → 测试验证
6. ki-manager → 知识沉淀
```

### Bug 工作流（快速修复）
```
1. 复现问题 → 确认问题存在
2. 定位根因 → 找到问题代码
3. 修复代码 → 最小改动原则
4. 验证修复 → 确认问题解决
5. (可选) ki-manager → 如果是典型坑，记录到 pitfalls.md
```

### Improvement 工作流（分析驱动）
```
1. 现状分析 → 度量当前状态
2. 方案设计 → 多方案对比
3. 实施改进 → 渐进式修改
4. 效果验证 → 对比前后差异
5. ki-manager → 记录到 component_patterns.md
```

## 分类输出模板

```markdown
## 任务分类结果

**原始请求**: [用户原话]

**分类结果**:
- 类型: Feature / Bug / Improvement / Question
- 领域: UI / Logic / Data / Infra
- 复杂度: 简单 / 中等 / 复杂

**推荐工作流**:
[根据分类选择对应工作流]

**涉及 Skills**:
[列出需要调用的 Skills]
```

## 分类规则

### 类型判断优先级
1. 明确关键词匹配（"bug"、"报错" → Bug）
2. 上下文分析（描述中有错误信息 → Bug）
3. 默认为 Feature（无明显特征时）

### 领域判断优先级
1. 文件路径分析（*.tsx → UI, *.py → Logic）
2. 技术栈关键词（TailwindCSS → UI, FastAPI → Logic）
3. 问题描述分析（"样式" → UI, "接口" → Logic）

## 与其他 Skills 的协作

| Skill | 协作场景 |
|:---|:---|
| **workflow-orchestrator** | 根据分类结果编排 Skills |
| **component-reuse-expert** | Feature 类型时触发 |
| **ki-manager** | Bug/Improvement 完成后可能触发 |
| **所有领域 Skills** | 根据领域分类触发对应 Skill |

---

## 进化日志

| 日期 | 更新内容 | 来源 |
|:---|:---|:---|
| 2025-12-28 | 初始版本：任务类型分类 + 领域分类 | 治理体系审核 |
