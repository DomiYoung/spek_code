---
name: skills-overview
description: |
  Skills 系统架构总览。提供所有 Skills 的协作关系和执行流程。
  当用户询问 Skills 系统、Claude 能力、或需要理解工作流程时触发。
  关键词：Skills、能力、工作流程、架构、协作、系统。
allowed-tools: Read
---

# Skills 系统架构总览

## 三层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     🎯 路由层 (Routing)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  workflow-router                                         │   │
│  │  智能分析任务 → 计算权重 → 路由到正确流程                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                    │
│         ┌──────────────────┴──────────────────┐                │
│         ↓                                      ↓                │
│   权重 ≥ 7                              权重 < 7                │
│   Spec-Kit 流程                         Feature Dev 专家        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     📚 知识层 (Knowledge)                        │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ reactflow   │ │ zustand     │ │ react-query │              │
│  │ patterns    │ │ patterns    │ │ patterns    │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ signalr     │ │ indexeddb   │ │ spec-kit    │              │
│  │ patterns    │ │ patterns    │ │ quality     │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                 │
│  这些 Skills 提供领域知识，被其他层引用                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     🚦 约束层 (Constraints)                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  code-quality-gates    →  写代码时                       │   │
│  │  commit-quality-gates  →  提交时                         │   │
│  │  review-quality-gates  →  交付前                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  tool-activation-banner  →  高亮显示工具调用             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 执行流程

### 开发任务流程

```
用户输入任务
      ↓
┌─ workflow-router ─────────────────────────────────────────┐
│                                                           │
│  1. 分析任务类型                                          │
│  2. 计算权重                                              │
│  3. 评估复杂度                                            │
│  4. 决定路由                                              │
│                                                           │
└───────────────────────────────────────────────────────────┘
      ↓
┌─────────────┬─────────────────────────────────────────────┐
│             │                                             │
│  权重 ≥ 7   │  权重 < 7                                   │
│             │                                             │
│  Spec-Kit   │  Feature Dev                                │
│  /speckit.* │  feature-dev:feature-dev [task]             │
│             │  feature-dev:code-explorer (代码分析)        │
│             │  feature-dev:code-architect (架构设计)       │
│             │                                             │
└─────────────┴─────────────────────────────────────────────┘
      ↓
┌─ 知识层 Skills 提供支持 ──────────────────────────────────┐
│                                                           │
│  根据任务类型自动引用:                                    │
│  • React/UI 相关 → reactflow-patterns, zustand-patterns   │
│  • API/数据 相关 → react-query-patterns, indexeddb-patterns│
│  • 实时通信 相关 → signalr-patterns                       │
│                                                           │
└───────────────────────────────────────────────────────────┘
      ↓
┌─ 约束层 Skills 检查 ──────────────────────────────────────┐
│                                                           │
│  写代码时 → code-quality-gates (红线检查)                 │
│  准备提交 → commit-quality-gates (格式检查)               │
│  最终交付 → review-quality-gates (全面审核)               │
│                                                           │
└───────────────────────────────────────────────────────────┘
      ↓
     完成
```

## Skills 清单

### 全局 Skills (`~/.claude/skills/`)

| Skill | 层级 | 用途 |
|-------|------|------|
| `workflow-router` | 路由 | 智能任务路由 |
| `tool-activation-banner` | 约束 | 工具调用高亮 |
| `code-quality-gates` | 约束 | 代码质量检查 |
| `commit-quality-gates` | 约束 | 提交规范检查 |
| `review-quality-gates` | 约束 | 最终交付审核 |
| `skills-overview` | 文档 | 本架构说明 |

### 项目 Skills (`.claude/skills/`)

| Skill | 层级 | 用途 |
|-------|------|------|
| `reactflow-patterns` | 知识 | ReactFlow 最佳实践 |
| `zustand-patterns` | 知识 | Zustand 状态管理 |
| `react-query-patterns` | 知识 | React Query 服务端状态 |
| `signalr-patterns` | 知识 | SignalR 实时通信 |
| `indexeddb-patterns` | 知识 | IndexedDB/Dexie 缓存 |
| `spec-quality-gates` | 知识 | Spec 文档质量验证 |

## MCP 工具集成

### 自动触发规则

| 场景 | 触发工具 | 横幅标识 |
|------|----------|----------|
| 复杂度 ≥ 3 | Sequential Thinking | 🧠 SEQUENTIAL |
| 涉及框架 API | Context7 | 📚 CONTEXT7 |
| 需要代码分析 | Serena | 🔍 SERENA |
| 任务管理 | Task Master | 📊 TASK MASTER |
| Feature Dev 专家 | 自动选择 | 🛠️ FEATURE-DEV |
| Spec-Kit 流程 | 自动选择 | 📋 SPEC-KIT |

## 快速参考

### 用户说什么 → Claude 做什么

| 用户输入 | 路由结果 |
|----------|----------|
| "实现 XXX 功能" | workflow-router → 评估权重 → 路由 |
| "修复 XXX bug" | → feature-dev:feature-dev (debug) |
| "优化性能" | → feature-dev:feature-dev --seq |
| "设计架构" | → /speckit.specify 或 feature-dev:code-architect |
| "帮我 review" | → review-quality-gates |
| "准备提交" | → commit-quality-gates + review |

### 横幅含义

```
🎯 SKILL       - Skill 被激活
🛠️ FEATURE-DEV - Feature Dev 专家模式
📋 SPEC-KIT    - Spec-Kit 规范流程
📚 CONTEXT7   - 官方文档查询
🔍 SERENA     - 语义代码分析
🧠 SEQUENTIAL - 深度推理模式
📊 TASK MASTER - 任务管理
```
