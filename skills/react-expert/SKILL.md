---
name: react-expert
description: "现代 React 开发专家。当用户需要：(1) 构建 React 组件 (2) 管理状态 useState/useReducer/Context/Zustand (3) 优化性能 memo/useMemo/useCallback (4) 使用 Hooks 模式 (5) 集成 TanStack Query/React Hook Form 时触发。"
---

# React Expert

## 决策树

```
状态类型 → 方案选择:
├── UI状态 (modal/tooltip) → useState
├── 表单 → React Hook Form + Zod
├── 服务端数据 → TanStack Query
├── 跨组件共享 → Context (简单) / Zustand (复杂)
└── 复杂全局 → Redux Toolkit
```

## 组件结构

```
components/
├── ui/        # 基础 (Button, Input)
├── layout/    # 布局 (Header, Sidebar)
├── features/  # 业务功能
└── views/     # 页面
```

## 核心模式

### 自定义 Hook 封装
```tsx
function useArticle(id: number) {
  const [data, setData] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchArticle(id).then(setData).finally(() => setLoading(false));
  }, [id]);
  return { data, loading };
}
```

### Compound Components
```tsx
<Card>
  <Card.Header>标题</Card.Header>
  <Card.Body>内容</Card.Body>
</Card>
```

## 性能预算

| 指标 | 目标 |
|------|------|
| LCP | < 2.5s |
| Bundle | < 200KB |

## 避免 ❌

- 组件内堆积逻辑 → 抽取 Hook
- Props drilling → Context/Zustand
- 过早优化 → 先测量后优化
