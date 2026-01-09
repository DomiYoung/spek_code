# Spek Code - Claude Code 配置框架

> 一套模块化的 Claude Code 配置系统，包含 Skills、专家系统、Spec-Kit 工作流等。

---

## 📁 目录结构

```
spek_code/
├── CLAUDE.md              # 入口文件（全局指令）
├── AGENTS.md              # Agent 路由索引
├── core/                  # 核心框架
│   ├── RULES.md           # 行为规则
│   ├── PRINCIPLES.md      # 工程原则
│   ├── FLAGS.md           # 模式标志
│   ├── MODES.md           # 行为模式
│   ├── MCP_GUIDE.md       # MCP 服务器指南
│   ├── DECISION_TREES.md  # 决策树
│   └── TOOL_SELECTION.md  # 工具选择
├── skills/                # 技能库
│   ├── workflow/          # 工作流技能
│   ├── experts/           # 专家技能
│   │   ├── frontend/      # 前端专家
│   │   ├── backend/       # 后端专家
│   │   ├── architect/     # 架构师
│   │   ├── product/       # 产品经理
│   │   └── ...
│   ├── patterns/          # 模式技能 (reactflow, zustand...)
│   └── tools/             # 工具技能 (xlsx, pdf...)
├── commands/              # Slash 命令
│   └── speckit.*.md       # Spec-Kit 命令集
├── configs/               # 配置文件
│   └── decision-trees/    # 决策树配置
├── rules/                 # 规则详情
├── templates/             # 格式模板
│   └── specify/           # Spec-Kit 模板
└── hooks/                 # 自动化钩子
```

---

## 🚀 快速开始

### 1. 安装

将配置复制到 `~/.claude/` 目录：

```bash
git clone https://github.com/DomiYoung/spek_code.git
cp -r spek_code/* ~/.claude/
```

### 2. 个性化配置

替换以下占位符：
- `YOUR_USERNAME` → 你的用户名
- `your-email@example.com` → 你的邮箱

---

## 🎯 核心功能

### 1. 权重评估系统

每个任务自动进行权重评估，决定执行路径：

| 权重 | Spec-Kit | Task Master | 说明 |
|------|----------|-------------|------|
| ≥ 7 | ✅ 强制 | ✅ 启用 | 复杂任务，需求锚点 |
| 5-6 | ⚠️ 建议 | ✅ 启用 | 中等任务 |
| 2-4 | ❌ 跳过 | ⚠️ 可选 | 简单任务 |

### 2. Spec-Kit 工作流

需求驱动的开发流程：

```
/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement
```

### 3. 专家路由系统

自动识别任务类型并路由到对应专家：

- **Frontend Expert**: React, TypeScript, UI/UX
- **Backend Expert**: API, 数据库, 服务端
- **Architect Expert**: 系统设计, 架构决策
- **Product Expert**: 需求分析, 用户故事

### 4. Skills 系统

50+ 专业技能模块：

| 类别 | 技能 |
|------|------|
| UI 框架 | `shadcn-ui`, `radix-ui`, `tailwindcss` |
| 状态管理 | `zustand`, `react-query` |
| 可视化 | `echarts`, `reactflow`, `mermaid` |
| 表单 | `react-hook-form`, `ag-grid` |
| 认证 | `oidc-auth`, `signalr` |
| 工具 | `pdf`, `xlsx`, `docx`, `pptx` |

---

## 🔧 配置说明

### MCP 服务器标志

| 标志 | 用途 |
|------|------|
| `--c7` | Context7 - 库文档查询 |
| `--seq` | Sequential - 多步推理 |
| `--magic` | Magic - UI 组件生成 |
| `--serena` | Serena - 符号操作 |
| `--play` | Playwright - 浏览器测试 |

### 思考深度

| 标志 | Token | 场景 |
|------|-------|------|
| `--think` | ~4K | 标准分析 |
| `--think-hard` | ~10K | 深度分析 |
| `--ultrathink` | ~32K | 系统级分析 |

---

## 📚 文档

- [核心规则](core/RULES.md)
- [工程原则](core/PRINCIPLES.md)
- [MCP 指南](core/MCP_GUIDE.md)
- [模式说明](core/MODES.md)
- [决策树](core/DECISION_TREES.md)

---

## 📄 License

MIT License

---

**Author**: DomiYoung | **Last Updated**: 2026-01-09
