---
name: react-query-patterns
type: Pattern
version: 1.0.0
description: |
  React Query 5.x 服务端状态管理。当涉及 API 请求、数据缓存、乐观更新、
  缓存失效时自动触发。
  关键词：React Query、useQuery、useMutation、缓存、staleTime、invalidate、API。
  【服务端状态核心】包含缓存策略、乐观更新、错误重试。
allowed-tools: Read, Grep, Glob
---

# React Query 5.x 服务端状态管理专家

> **核心理念**：服务端状态分离，SWR 缓存策略，精确失效控制。
> **来源**：[TanStack Query 官方文档](https://tanstack.com/query)、[React Query 最佳实践](https://tkdodo.eu/blog/)

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **queryKey 必须含参数** | 动态请求参数必须包含在 queryKey | `grep -rE "queryKey:\s*\[['\"][^]]+\].*queryFn.*\(" src/ --include="*.ts"` |
| **enabled 必须检查** | 可选参数必须用 enabled 控制 | `grep -rE "queryKey:.*undefined\|null" src/ --include="*.ts"` |
| **mutation 必须有 onError** | 写操作必须处理错误 | `grep -rE "useMutation\(\{[^}]*\}\)" src/ \| grep -v "onError"` |
| **invalidateQueries 精确匹配** | 失效范围必须精确 | 代码审查：检查 queryKey 层级 |
| **staleTime 必须配置** | 禁止默认 0（无限制刷新） | `grep -rE "useQuery\(\{[^}]*\}\)" src/ \| grep -v "staleTime"` |
| **gcTime 合理设置** | 生产环境不应无限缓存 | 代码审查：检查 gcTime 配置 |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ queryKey 不够具体导致缓存冲突 ⭐⭐⭐⭐⭐

**问题**: 不同参数用相同 key，缓存数据混乱
**检测**: `grep -rE "queryKey:\s*\[['\"][^,\]]+['\"]]\s*," src/ --include="*.ts"`
**修正**: 将所有动态参数包含在 queryKey

```typescript
// ❌ 错误 - 不同 id 用相同 key
useQuery({ queryKey: ['workflow'], queryFn: () => api.get(id) });
useQuery({ queryKey: ['workflow'], queryFn: () => api.get(otherId) });
// 结果：缓存冲突，显示错误数据！

// ✅ 正确 - 包含参数
useQuery({ queryKey: ['workflow', id], queryFn: () => api.get(id) });
```

### ❌ queryFn 使用未包含在 queryKey 的变量 ⭐⭐⭐⭐⭐

**问题**: 变量变化但查询不重新执行
**检测**: 代码审查 - 比对 queryFn 参数和 queryKey
**修正**: 将所有 queryFn 依赖项加入 queryKey

```typescript
// ❌ 错误 - filter 变化但 queryKey 不变
const { data } = useQuery({
  queryKey: ['workflows'],
  queryFn: () => api.getWorkflows({ filter }),  // filter 变化不会重新请求！
});

// ✅ 正确 - filter 包含在 queryKey
const { data } = useQuery({
  queryKey: ['workflows', filter],
  queryFn: () => api.getWorkflows({ filter }),
});
```

### ❌ 缺少 enabled 导致无效请求 ⭐⭐⭐⭐⭐

**问题**: 参数为 undefined 时仍发起请求
**检测**: `grep -rE "queryFn:.*\w+!" src/ --include="*.ts" | grep -v "enabled"`
**修正**: 添加 enabled 条件检查

```typescript
// ❌ 错误 - id 可能是 undefined
useQuery({
  queryKey: ['workflow', id],
  queryFn: () => api.getWorkflow(id!),  // 可能请求 undefined！
});

// ✅ 正确 - 使用 enabled
useQuery({
  queryKey: ['workflow', id],
  queryFn: () => api.getWorkflow(id!),
  enabled: !!id,  // id 存在才执行
});
```

### ❌ useMutation 未处理错误 ⭐⭐⭐⭐

**问题**: 请求失败无反馈，用户不知发生了什么
**检测**: `grep -rE "useMutation\(\{" src/ -A 10 | grep -v "onError"`
**修正**: 添加 onError 回调

```typescript
// ❌ 错误 - 无错误处理
const mutation = useMutation({
  mutationFn: (data) => api.createWorkflow(data),
  onSuccess: () => queryClient.invalidateQueries(['workflows']),
  // 失败时用户毫无感知！
});

// ✅ 正确 - 完整的错误处理
const mutation = useMutation({
  mutationFn: (data) => api.createWorkflow(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['workflows'] });
    message.success('创建成功');
  },
  onError: (error) => {
    message.error(`创建失败：${error.message}`);
  },
});
```

### ❌ staleTime 为 0 导致过度请求 ⭐⭐⭐⭐

**问题**: 每次组件挂载都重新请求，浪费带宽
**检测**: `grep -rE "useQuery\(\{[^}]*\}\)" src/ | grep -v "staleTime"`
**修正**: 根据业务设置合理的 staleTime

```typescript
// ❌ 错误 - 默认 staleTime = 0
useQuery({
  queryKey: ['workflows'],
  queryFn: fetchWorkflows,
  // 每次组件挂载都请求！
});

// ✅ 正确 - 设置合理的 staleTime
useQuery({
  queryKey: ['workflows'],
  queryFn: fetchWorkflows,
  staleTime: 5 * 60 * 1000,  // 5 分钟内不重新请求
});
```

### ❌ invalidateQueries 范围过大 ⭐⭐⭐

**问题**: 失效整个 queryKey 前缀，导致不必要的重新请求
**检测**: `grep -rE "invalidateQueries.*queryKey:\s*\[['\"]" src/ --include="*.ts"`
**修正**: 使用精确匹配或 exact 选项

```typescript
// ❌ 错误 - 失效所有 workflow 相关查询
queryClient.invalidateQueries({ queryKey: ['workflow'] });
// 连 ['workflow', 'templates'] 都失效了！

// ✅ 正确 - 精确失效
queryClient.invalidateQueries({ queryKey: ['workflow', id] });

// ✅ 或使用 exact 选项
queryClient.invalidateQueries({
  queryKey: ['workflows'],
  exact: true,  // 只失效精确匹配的查询
});
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### 何时使用 React Query vs Zustand

```
React Query（服务端状态）:
├─ API 请求结果
├─ 需要缓存的远程数据
├─ 需要自动刷新的数据
└─ 多组件共享的服务端数据

Zustand（客户端状态）:
├─ UI 状态（弹窗、选中项）
├─ 表单状态
├─ 本地计算结果
└─ 不需要持久化的临时状态
```

### useQuery 标准模板

```typescript
import { useQuery } from '@tanstack/react-query';

interface UseWorkflowOptions {
  id: string;
  enabled?: boolean;
}

export function useWorkflow({ id, enabled = true }: UseWorkflowOptions) {
  return useQuery({
    queryKey: ['workflow', id],
    queryFn: () => api.getWorkflow(id),
    enabled: enabled && !!id,
    staleTime: 5 * 60 * 1000,      // 5 分钟
    gcTime: 30 * 60 * 1000,         // 30 分钟
    retry: 2,                        // 失败重试 2 次
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

// 组件中使用
function WorkflowDetail({ id }: { id: string }) {
  const { data, isLoading, error, refetch } = useWorkflow({ id });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} onRetry={refetch} />;
  if (!data) return <EmptyState />;

  return <WorkflowCard workflow={data} />;
}
```

### useMutation 标准模板

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useUpdateWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateWorkflowInput }) =>
      api.updateWorkflow(id, data),

    onMutate: async ({ id, data }) => {
      // 1. 取消正在进行的请求
      await queryClient.cancelQueries({ queryKey: ['workflow', id] });

      // 2. 保存旧数据（用于回滚）
      const previousData = queryClient.getQueryData(['workflow', id]);

      // 3. 乐观更新
      queryClient.setQueryData(['workflow', id], (old: Workflow) => ({
        ...old,
        ...data,
      }));

      return { previousData };
    },

    onError: (err, { id }, context) => {
      // 失败时回滚
      if (context?.previousData) {
        queryClient.setQueryData(['workflow', id], context.previousData);
      }
      message.error(`更新失败：${err.message}`);
    },

    onSuccess: (_, { id }) => {
      message.success('更新成功');
    },

    onSettled: (_, __, { id }) => {
      // 无论成功失败，都重新获取最新数据
      queryClient.invalidateQueries({ queryKey: ['workflow', id] });
    },
  });
}
```

### 依赖查询模板

```typescript
function UserWorkflows() {
  // 第一个查询：获取用户
  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: fetchCurrentUser,
    staleTime: 10 * 60 * 1000,
  });

  // 第二个查询：依赖用户 ID
  const { data: workflows } = useQuery({
    queryKey: ['workflows', 'user', user?.id],
    queryFn: () => fetchUserWorkflows(user!.id),
    enabled: !!user?.id,  // 只有 user 存在时才执行
    staleTime: 5 * 60 * 1000,
  });

  // ...
}
```

### 无限滚动模板

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';
import { Virtuoso } from 'react-virtuoso';

export function useInfiniteWorkflows(filter?: WorkflowFilter) {
  return useInfiniteQuery({
    queryKey: ['workflows', 'infinite', filter],
    queryFn: ({ pageParam }) =>
      api.getWorkflows({ cursor: pageParam, filter, limit: 20 }),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    staleTime: 5 * 60 * 1000,
  });
}

function InfiniteWorkflowList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteWorkflows();

  const allItems = data?.pages.flatMap((page) => page.items) ?? [];

  return (
    <Virtuoso
      data={allItems}
      endReached={() => hasNextPage && !isFetchingNextPage && fetchNextPage()}
      itemContent={(_, item) => <WorkflowCard workflow={item} />}
      components={{
        Footer: () => isFetchingNextPage ? <Spinner /> : null,
      }}
    />
  );
}
```

### 缓存策略说明

```typescript
/*
 * staleTime vs gcTime 理解：
 *
 * staleTime: 数据多久后变"陈旧"（触发后台刷新）
 * gcTime: 数据在缓存中保留多久（即使没有订阅者）
 *
 * 场景：用户打开页面，5 分钟后再次访问
 *
 * 1. staleTime 内（0-5min）：
 *    → 直接用缓存，不请求
 *
 * 2. staleTime 后，gcTime 内（5-30min）：
 *    → 先显示缓存（SWR），后台请求新数据
 *
 * 3. gcTime 后（>30min）：
 *    → 缓存被清除，显示 loading，重新请求
 */

// 推荐配置
const defaultQueryOptions = {
  staleTime: 5 * 60 * 1000,   // 5 分钟
  gcTime: 30 * 60 * 1000,     // 30 分钟
  retry: 2,
  refetchOnWindowFocus: false, // 生产环境通常关闭
};
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前运行

### 自动审计脚本

```bash
#!/bin/bash
# react-query-audit.sh

echo "🔍 React Query Expert Audit..."

# 1. 检查 queryKey 是否包含动态参数
STATIC_KEY=$(grep -rE "queryKey:\s*\[['\"][^,\]]+['\"]]\s*," src/ --include="*.ts" 2>/dev/null | \
  grep -v "staleTime\|enabled\|gcTime")
if [ -n "$STATIC_KEY" ]; then
  echo "⚠️ 发现可能缺少动态参数的 queryKey:"
  echo "$STATIC_KEY"
fi

# 2. 检查 useMutation 是否有 onError
NO_ERROR=$(grep -rE "useMutation\(\{" src/ --include="*.ts" -A 15 2>/dev/null | \
  grep -B 15 "mutationFn" | grep -L "onError")
if [ -n "$NO_ERROR" ]; then
  echo "❌ 发现 useMutation 未处理 onError"
  exit 1
fi

# 3. 检查是否使用非断言访问可选参数
UNSAFE_ACCESS=$(grep -rE "queryFn:.*\w+!" src/ --include="*.ts" 2>/dev/null | grep -v "enabled")
if [ -n "$UNSAFE_ACCESS" ]; then
  echo "⚠️ 发现可能缺少 enabled 检查:"
  echo "$UNSAFE_ACCESS"
fi

# 4. 检查 staleTime 配置
NO_STALE=$(grep -rE "useQuery\(\{" src/ --include="*.ts" -A 5 2>/dev/null | \
  grep -B 5 "queryFn" | grep -L "staleTime")
if [ -n "$NO_STALE" ]; then
  echo "⚠️ 发现 useQuery 未配置 staleTime"
fi

# 5. 检查 invalidateQueries 精确性
BROAD_INVALIDATE=$(grep -rE "invalidateQueries\(\{[^}]*queryKey:\s*\[['\"][^,\]]+['\"]]\s*\}" src/ 2>/dev/null | \
  grep -v "exact")
if [ -n "$BROAD_INVALIDATE" ]; then
  echo "⚠️ 发现可能过于宽泛的 invalidateQueries:"
  echo "$BROAD_INVALIDATE"
fi

echo "✅ React Query Audit Passed"
```

### 交付检查清单

```
□ queryKey 包含所有动态参数
□ queryFn 依赖项全部在 queryKey 中
□ 可选参数使用 enabled 控制
□ useMutation 有 onError 处理
□ useQuery 配置了 staleTime
□ invalidateQueries 范围精确
□ 乐观更新有 rollback 机制
□ 复杂查询封装为 custom hooks
□ 错误重试配置合理（retry/retryDelay）
□ 区分服务端状态 vs 客户端状态
```

### queryKey 规范检查

| 检查项 | 期望格式 |
|--------|----------|
| 列表查询 | `['workflows', filter]` |
| 单项查询 | `['workflow', id]` |
| 嵌套资源 | `['workflow', workflowId, 'nodes']` |
| 用户相关 | `['workflows', 'user', userId]` |
| 无限滚动 | `['workflows', 'infinite', filter]` |

---

## 🔗 与全局 Skills 协作

### 触发路径

```
用户: "优化 API 请求" / "添加缓存" / "react query"
        ↓
workflow-orchestrator → expert-router
        ↓
本 Skill 提供 React Query 最佳实践
```

### 协作关系

| Skill | 协作方式 |
|-------|----------|
| `zustand-patterns` | 区分客户端/服务端状态边界 |
| `indexeddb-patterns` | 双层缓存：React Query + IndexedDB |
| `signalr-patterns` | 实时数据与缓存同步 |
| `code-quality-gates` | 检查 queryKey 规范、enabled 使用 |
| `frontend-expert` | 提供 React 性能优化指导 |

### 关联文件

- `src/features/*/hooks/use*.ts`（数据获取 hooks）
- `src/api/*.ts`（API 封装）

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 无泛泛而谈的建议（"小心"、"注意"等）
- [x] 代码块可直接复制使用
