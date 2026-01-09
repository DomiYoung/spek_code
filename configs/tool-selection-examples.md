# 工具选择场景示例

## 场景 1: 简单 Bug 修复

```
用户: "登录按钮点击没反应"
    ↓
workflow-router: 自动激活（检测到"没反应"关键词）
├─ 任务类型: Bug修复
├─ 权重评估: 2（简单 Bug）
├─ 专家选择: troubleshoot
├─ Spec-Kit: ❌ 跳过
└─ Task Master: ❌ 跳过
    ↓
自动执行 → 无需用户输入任何命令
```

---

## 场景 2: 新功能开发

```
用户: "添加用户权限管理系统"
    ↓
workflow-router: 自动激活（检测到"添加"关键词）
├─ 任务类型: 新功能
├─ 权重评估: 10（新功能 + 架构变更）
├─ 专家选择: backend + security
├─ Spec-Kit: ✅ 强制（权重 ≥ 7）
└─ Task Master: ✅ 启用（>5 步）
    ↓
自动进入 Spec-Kit 5 步流程
```

---

## 场景 3: 代码分析

```
用户: "帮我理解一下认证模块"
    ↓
workflow-router: 自动激活（检测到"理解"关键词）
├─ 任务类型: 分析
├─ 权重评估: 0（纯分析）
├─ 专家选择: analyze
├─ MCP 标志: --think-hard --serena
├─ Spec-Kit: ❌ 跳过
└─ Task Master: ❌ 跳过
    ↓
自动执行分析
```

---

## 场景 4: 性能优化重构

```
用户: "列表渲染太慢，需要支持万级数据"
    ↓
workflow-router: 自动激活（检测到"慢"关键词）
├─ 任务类型: 优化
├─ 权重评估: 8（重构 + 架构变更）
├─ 专家选择: performance + frontend
├─ MCP 标志: --seq --c7
├─ Spec-Kit: ✅ 强制（权重 ≥ 7）
└─ Task Master: ✅ 启用（多步骤）
    ↓
自动进入 Spec-Kit 流程
```
