# 决策树 2: 专家路由 (Expert Router)

**目的**: 决定 SuperPowers 专家（1% 原则）

> **Note**: 旧版 `/sc` 命令已废弃，统一使用 `feature-dev` 插件的 skills

## 决策流程图

```
START: 分析任务关键词
│
├─ 包含【UI/组件/样式/CSS/React/Vue/前端】？
│   └─ YES → 🎨 frontend 专家
│            feature-dev:feature-dev
│
├─ 包含【API/数据库/后端/服务端/Node/Python】？
│   └─ YES → 🔧 backend 专家
│            feature-dev:feature-dev
│
├─ 包含【安全/认证/漏洞/权限/加密】？
│   └─ YES → 🛡️ security 专家
│            feature-dev:feature-dev
│
├─ 包含【性能/优化/卡顿/慢/内存/渲染】？
│   └─ YES → ⚡ performance 专家
│            feature-dev:feature-dev
│
├─ 包含【Bug/报错/崩溃/不工作/异常】？
│   └─ YES → 🔍 troubleshoot 模式
│            feature-dev:feature-dev
│
├─ 包含【分析/理解/架构/设计/评估】？
│   └─ YES → 📊 analyze 模式
│            feature-dev:code-explorer
│
└─ 默认
    └─ → 🚀 implement 模式
         feature-dev:feature-dev
```

## 专家匹配速查

| 关键词 | 专家 | Skill |
|--------|------|-------|
| UI, 组件, 样式, React, Vue | frontend | `feature-dev:feature-dev` |
| API, 数据库, 后端 | backend | `feature-dev:feature-dev` |
| 安全, 认证, 漏洞 | security | `feature-dev:feature-dev` |
| 性能, 优化, 卡顿 | performance | `feature-dev:feature-dev` |
| Bug, 报错, 崩溃 | troubleshoot | `feature-dev:feature-dev` |
| 分析, 架构, 设计 | analyze | `feature-dev:code-explorer` |
| 默认 | implement | `feature-dev:feature-dev` |

## 1% 原则

> 如果有 1% 的可能性某个专家适用，必须调用它。

多个专家领域可以在同一个 skill 调用中组合分析。
