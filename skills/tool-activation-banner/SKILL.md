---
name: tool-activation-banner
description: |
  工具调用高亮提示。确保 Claude 在使用核心工具时显示醒目横幅。
  【强制规则】使用 Feature-Dev、Context7、Spec-Kit、Serena、Sequential 时必须显示。
  每次调用 MCP 工具或 Slash Command 时自动触发。
allowed-tools: "*"
---

# 工具调用高亮提示

## 核心规则

当调用以下工具时，**必须先输出高亮横幅**：

## 横幅格式（紧凑版）

### 单行横幅（推荐）

```
▶ 🎯 SKILL: workflow-router | 智能任务路由
▶ 🛠️ FEATURE-DEV: frontend | React 组件架构
▶ 🛠️🛠️ FEATURE-DEV: frontend + backend | 多专家协作
▶ 📋 SPEC-KIT: specify | 需求规范阶段
▶ 📚 CONTEXT7: react-query | 官方文档查询
▶ 🔍 SERENA: find_symbol | 语义代码分析
▶ 🧠 SEQUENTIAL: 深度推理 | 复杂问题分析
▶ 📊 TASK MASTER: get_tasks | 任务管理
```

### 框式横幅（重要操作）

仅在以下情况使用框式横幅：
- Spec-Kit 流程启动
- 多专家协作
- 重大决策点

```
╔═══════════════════════════════════════════════╗
║  🛠️ FEATURE-DEV 多专家协作                    ║
║  专家: frontend + performance                 ║
║  MCP: --seq --c7                              ║
╚═══════════════════════════════════════════════╝
```

## 横幅映射表

| 工具/命令 | 横幅 | 说明 |
|-----------|------|------|
| Skill 激活 | `▶ 🎯 SKILL: [name]` | Skill 被触发 |
| `feature-dev:feature-dev` | `▶ 🛠️ FEATURE-DEV: [task]` | 功能开发 |
| `feature-dev:code-explorer` | `▶ 🔍 CODE-EXPLORER: [scope]` | 代码分析 |
| `feature-dev:code-architect` | `▶ 🏗️ CODE-ARCHITECT: [design]` | 架构设计 |
| `/speckit.*` | `▶ 📋 SPEC-KIT: [phase]` | Spec 流程 |
| `mcp__context7__*` | `▶ 📚 CONTEXT7: [topic]` | 文档查询 |
| `mcp__serena__*` | `▶ 🔍 SERENA: [operation]` | 代码分析 |
| `mcp__sequential-thinking__*` | `▶ 🧠 SEQUENTIAL: [purpose]` | 深度推理 |
| `mcp__task-master-ai__*` | `▶ 📊 TASK MASTER: [operation]` | 任务管理 |

## MCP 增强标志显示

当 Feature Dev 使用 MCP 增强时，追加显示：

```
▶ 🛠️ FEATURE-DEV: frontend | --seq --c7
                             ↑ MCP 标志
```

## 使用示例

### 示例1：简单任务

```
用户: 帮我看看 useQuery 怎么用

Claude:
▶ 📚 CONTEXT7: @tanstack/react-query | useQuery

[调用 mcp__context7__get-library-docs]

根据官方文档...
```

### 示例2：复杂任务

```
用户: 实现虚拟滚动的消息列表

Claude:
▶ 🎯 SKILL: workflow-router | 任务路由分析

## 📍 任务路由分析
| 维度 | 分析结果 |
|------|----------|
| 任务类型 | 新功能（前端组件） |
| 复杂度 | 4（性能敏感） |
| 权重 | 5 |

╔═══════════════════════════════════════════════╗
║  🛠️ FEATURE-DEV 多专家协作                    ║
║  专家: frontend + performance                 ║
║  MCP: --seq --c7                              ║
╚═══════════════════════════════════════════════╝

▶ 🧠 SEQUENTIAL: 组件架构分析

[深度分析...]
```

### 示例3：Bug 修复

```
用户: 刷新后子节点丢失

Claude:
▶ 🎯 SKILL: workflow-router | Bug 修复路由
▶ 🛠️ FEATURE-DEV: debug | 根因分析

[开始分析...]
```

## 不需要横幅的操作

以下基础操作**不需要**横幅：
- `Read` / `Write` / `Edit`
- `Glob` / `Grep`
- `Bash`（简单命令）
- `TodoWrite`

## 验证清单

每次使用核心工具时：
- [ ] 显示了对应横幅？
- [ ] 横幅标识正确？
- [ ] 用户能看懂正在用什么？
