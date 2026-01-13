# Pre-Implementation Checklist

> 代码编写前的强制检查清单，由 RULES.md 引用

## 检查清单

```
┌─ Pre-Implementation Check ────────────────────┐
│ □ 需求明确？         → [是/否，否则 brainstorm]│
│ □ task_plan.md 存在？→ [是/否，否则 planning] │
│ □ 复用检查？         → [是/否，列出可复用组件] │
│ □ 权重评估？         → [已完成/待完成]         │
│ □ 目录结构正确？     → [.planning/]           │
└───────────────────────────────────────────────┘
```

## Hook 强制拦截

- `enforce-workflow.py`: 代码文件编写前检查 `.planning/` 是否存在 task_plan.md
- 未通过检查 → 阻止操作 + 提示创建 task_plan.md

## 豁免方式

- 在请求中包含 "跳过检查" 或 "skip-check"
- 紧急修复使用 "hotfix" 关键词
- 测试文件、配置文件、文档文件自动豁免

## 豁免路径

自动跳过检查的目录/文件：
- `.planning/` - planning 目录本身
- `.claude/` - Claude 配置目录
- `docs/` - 文档目录
- `scripts/` - 脚本目录
- `__tests__/` - 测试目录
- `*.test.ts`, `*.spec.ts` - 测试文件
- `*.md`, `*.json`, `*.yaml` - 配置/文档文件

## 流程强制顺序

```
用户需求 → 权重评估 → [权重≥3] → planning-with-files 流程
                              ↓
                         brainstorm → task_plan.md → 执行
                              ↓
                    .planning/task_plan.md 存在
                              ↓
                    Hook 验证通过 → 允许编写代码
```
