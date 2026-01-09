---
name: typescript-expert
description: "TypeScript 专家。当用户需要：(1) 设计类型系统 (2) 使用泛型/工具类型 (3) 类型收窄/类型守卫 (4) 配置 strict 模式 (5) 解决类型错误时触发。"
---

# TypeScript Expert

## 类型选择

```
Interface → 对象形状，可扩展 (extend)
Type     → 联合/交叉/工具类型
```

## 常用工具类型

| 工具 | 用途 |
|------|------|
| `Partial<T>` | 所有可选 |
| `Required<T>` | 所有必需 |
| `Pick<T, K>` | 选取属性 |
| `Omit<T, K>` | 排除属性 |
| `Record<K, V>` | 键值映射 |

## 核心模式

### Discriminated Unions
```typescript
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: string };
```

### Type Guards
```typescript
function isUser(obj: unknown): obj is User {
  return typeof obj === "object" && obj !== null && "id" in obj;
}
```

### Branded Types
```typescript
type UserId = number & { __brand: "UserId" };
```

## 严格配置

```json
{ "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true } }
```

## 避免 ❌

- `any` → 用 `unknown` + 类型收窄
- `as` 断言滥用 → 用类型守卫
- 非空断言 `!` → 用可选链 `?.`
