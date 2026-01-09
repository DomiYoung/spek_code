# 决策树自动执行示例

> **Note**: 旧版 `/sc` 和 `/smart-workflow` 命令已废弃，统一使用 `feature-dev` 插件的 skills

## 示例 1: 简单 Bug

```
用户: "登录按钮点击没反应"

决策树 1 (复杂度):
├─ Q1: 分析任务？ → NO
├─ Q2: 样式文档？ → NO
├─ Q3: 新功能？ → NO
├─ Q4: API变更？ → NO
├─ Q5: >5文件？ → NO
├─ Q6: 3-5文件？ → NO
└─ 默认 → 权重 2, 简单路径

决策树 2 (专家):
├─ Bug 关键词 → YES
└─ → feature-dev:feature-dev

决策树 3 (标志):
├─ 浏览器调试？ → 可能
└─ → --chrome (建议)

最终执行: feature-dev:feature-dev bug修复 登录按钮点击没反应 --chrome
```

## 示例 2: 新功能开发

```
用户: "添加用户权限管理系统"

决策树 1 (复杂度):
├─ Q1: 分析任务？ → NO
├─ Q2: 样式文档？ → NO
├─ Q3: 新功能？ → YES ✓
└─ → 权重 10, 重量路径, 强制 Spec-Kit

决策树 2 (专家):
├─ 后端 + 安全关键词 → YES
└─ → feature-dev:feature-dev (backend + security)

决策树 3 (标志):
├─ 多组件/架构级？ → YES
└─ → --think-hard

最终执行:
1. 启动 Spec-Kit 5 步流程
2. feature-dev:feature-dev 权限管理系统 --think-hard
```

## 示例 3: 代码分析

```
用户: "分析这个模块的架构设计"

决策树 1 (复杂度):
├─ Q1: 分析任务？ → YES ✓
└─ → 权重 0, 轻量路径, 跳过 Spec-Kit

决策树 2 (专家):
├─ 分析关键词 → YES
└─ → feature-dev:code-explorer

决策树 3 (标志):
├─ 架构级分析？ → YES
└─ → --think-hard --serena

最终执行: feature-dev:code-explorer --think-hard --serena src/模块路径
```

## 示例 4: 性能优化

```
用户: "列表渲染太慢，需要虚拟滚动"

决策树 1 (复杂度):
├─ Q1: 分析任务？ → NO
├─ Q2: 样式文档？ → NO
├─ Q3: 新功能？ → 可能
├─ Q4: API变更？ → NO
├─ Q5: >5文件？ → NO
├─ Q6: 3-5文件？ → YES
└─ → 权重 5, 中等路径

决策树 2 (专家):
├─ 性能关键词 "慢" → YES
└─ → feature-dev:feature-dev (performance)

决策树 3 (标志):
├─ 前端渲染？ → YES
└─ → --chrome

最终执行: feature-dev:feature-dev 优化拓展 列表虚拟滚动 --chrome
```

## 效能指标

| 指标 | 目标 | 说明 |
|------|------|------|
| **Early Exit Rate** | ≥ 80% | 前 2 个问题决定大多数任务 |
| **决策时间** | < 30 秒 | 快速路由，不阻塞执行 |
| **准确率** | ≥ 90% | 正确选择工具组合 |
| **深度** | ≤ 5 层 | 避免过度复杂 |
