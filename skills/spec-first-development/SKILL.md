---
name: spec-first-development
description: "Spec-First (Spec-Kit) 开发方法论 - 规范驱动的开发流程，确保所有功能有完整规范后再编码"
---

# Spec-First Development (Spec-Kit)

## 核心宪法

> **拒绝在没有规范的情况下编写业务代码。**
> 
> API 契约是前后端协作的**唯一真理来源**。

## Spec-Kit 四件套

```
specs/{feature_id}/
├── spec.md           # 功能需求 & 用户故事
├── data-model.md     # 数据库模式 / 数据结构
├── contracts/        
│   └── api-spec.json # OpenAPI 契约 (唯一真理)
└── plan.md           # 实施步骤
```

### 1. spec.md 模板
```markdown
# Specification: {Feature Name}

## 1. Background
[为什么需要这个功能]

## 2. User Stories
- As a [role], I want [feature] so that [benefit].

## 3. Functional Requirements
### 3.1 [Component Name]
- Requirement 1
- Requirement 2

## 4. UI/UX Requirements
[界面设计要求]

## 5. Technical Logic
[技术实现逻辑]
```

### 2. data-model.md 模板
```markdown
# Data Model: {Feature Name}

## Entities

### Entity1
| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| name | string | ... |

## Relationships
[Entity1] 1:N [Entity2]
```

### 3. api-spec.json (OpenAPI)
```json
{
  "openapi": "3.0.0",
  "paths": {
    "/api/resource/{id}": {
      "get": {...}
    }
  }
}
```

### 4. plan.md 模板
```markdown
# Implementation Plan

## Phase 1: [Phase Name]
- [ ] Task 1
- [ ] Task 2

## Verification
- [ ] 测试方法
```

## 工作流程

```
1. Discovery   → 探索现有代码/模式
      ↓
2. Design      → 创建 Spec-Kit 四件套
      ↓
3. Agreement   → 前后端对齐 api-spec.json
      ↓
4. Execution   → 按 plan.md 实施
      ↓
5. Verification → 对照需求验证
```

## 强制规则

✅ **必须做**
- 先规范，后编码
- API 契约冻结后才能开发
- 每个 Phase 完成后更新 task.md

❌ **禁止做**
- 跳过规范直接开发
- 边开发边改契约
- 口头约定 API 格式
