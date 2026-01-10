---
name: frontend-expert
description: |
  前端开发专家 - 基于 React/Vue 生产级最佳实践。
  ① 帮我干什么：组件设计、状态管理、性能优化、类型安全
  ② 什么时候出场：涉及 React、Vue、CSS、UI、组件、样式、响应式、动画时自动调用
  ③ 和项目有无关系：适用于所有前端项目，是全局通用的前端专家
  关键词：React、Vue、CSS、UI、组件、样式、响应式、动画、TypeScript、Hooks
allowed-tools: "*"
---

# Frontend Expert（前端开发专家）

> **核心理念**：类型安全第一，用户体验至上。
> **来源**：[React 官方文档](https://react.dev/)、[Vue 官方文档](https://vuejs.org/)、[Web.dev](https://web.dev/)

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **禁止 any** | 零 `any` 类型（除非有注释说明） | `grep -rE ": any[^a-zA-Z]" src/ --include="*.ts" --include="*.tsx"` |
| **禁止 ts-ignore** | 不允许跳过类型检查 | `grep -r "@ts-ignore\|@ts-expect-error" src/` |
| **禁止 console.log** | 生产代码无调试日志 | `grep -r "console.log" src/ --include="*.ts" --include="*.tsx"` |
| **错误边界** | 关键组件有 ErrorBoundary | 代码审查：检查路由级组件 |
| **加载状态** | 异步操作有 loading/error/empty | UI 审查：检查 useQuery/useMutation |
| **无障碍** | 语义化标签、ARIA、键盘可达 | `npx axe-core` 或 Lighthouse Accessibility |
| **类型完整** | Props/State 有明确类型定义 | `tsc --noEmit` 无错误 |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ React: useState 解构丢弃变量

**问题**: 生产环境 `ReferenceError: xxx is not defined`
**检测**: `grep -rE "const \[,\s*set" src/ --include="*.tsx"`
**修正**: 保留需要使用的状态变量

```tsx
// ❌ 错误
const [, setIframeReady] = useState(false);
{!iframeReady && <LoadingSpinner />}  // ReferenceError!

// ✅ 正确
const [iframeReady, setIframeReady] = useState(false);
```

### ❌ React: Stale Closure（过期闭包）

**问题**: 事件处理器或定时器中状态总是旧值
**检测**: `grep -rE "setInterval.*useState|setTimeout.*useState" src/`
**修正**: 使用函数式更新 `setCount(prev => prev + 1)` 或 useRef

```tsx
// ❌ 错误 - count 始终是 0
useEffect(() => {
  setInterval(() => setCount(count + 1), 1000);
}, []);

// ✅ 正确 - 函数式更新
useEffect(() => {
  const timer = setInterval(() => setCount(prev => prev + 1), 1000);
  return () => clearInterval(timer);
}, []);
```

### ❌ React: useEffect 清理函数遗漏

**问题**: 内存泄漏、组件卸载后仍 setState
**检测**: `grep -rE "useEffect.*fetch.*setState" src/ --include="*.tsx"` + 检查是否有 return
**修正**: 使用 AbortController 或 isMounted 标志

```tsx
// ❌ 错误
useEffect(() => {
  fetch('/api').then(r => r.json()).then(setData);
}, []);

// ✅ 正确
useEffect(() => {
  const controller = new AbortController();
  fetch('/api', { signal: controller.signal })
    .then(r => r.json()).then(setData)
    .catch(e => { if (e.name !== 'AbortError') throw e; });
  return () => controller.abort();
}, []);
```

### ❌ React: 条件调用 Hooks

**问题**: `Rendered more hooks than previous render` 错误
**检测**: `grep -rE "if.*useState|if.*useEffect" src/ --include="*.tsx"`
**修正**: Hooks 必须无条件调用，在 JSX 中条件渲染

```tsx
// ❌ 错误
if (showExtra) {
  const [extra, setExtra] = useState('');
}

// ✅ 正确
const [extra, setExtra] = useState('');
{showExtra && <span>{extra}</span>}
```

### ❌ React: key 使用 index

**问题**: 列表重排/删除后状态混乱
**检测**: `grep -rE "key={index}|key=\{i\}" src/ --include="*.tsx"`
**修正**: 使用唯一稳定 ID

```tsx
// ❌ 错误
{items.map((item, index) => <Item key={index} />)}

// ✅ 正确
{items.map(item => <Item key={item.id} />)}
```

### ❌ React: useCallback/useMemo 依赖不完整

**问题**: 回调使用过期数据
**检测**: ESLint `react-hooks/exhaustive-deps` 规则
**修正**: 完整声明依赖数组

```tsx
// ❌ 错误
const handleSubmit = useCallback(() => submitForm(formData), []);

// ✅ 正确
const handleSubmit = useCallback(() => submitForm(formData), [formData]);
```

### ❌ Vue: 响应式丢失

**问题**: 数据更新但视图不刷新
**检测**: `grep -rE "const \{.*\} = reactive" src/ --include="*.vue"`
**修正**: 使用 toRefs 保持响应式

```vue
// ❌ 错误 - 解构丢失响应式
const { count } = reactive({ count: 0 });

// ✅ 正确
const { count } = toRefs(reactive({ count: 0 }));
```

### ❌ Vue: watch 无法触发

**问题**: 深层属性变化 watch 不触发
**检测**: `grep -rE "watch\(state\." src/ --include="*.vue"`
**修正**: 使用 getter 函数或 deep: true

```vue
// ❌ 错误
watch(state.nested.count, fn);

// ✅ 正确
watch(() => state.nested.count, fn);
```

### ❌ Vue: v-for 与 v-if 同时使用

**问题**: Vue 3 中 v-if 优先级高，无法访问循环变量
**检测**: `grep -rE "v-for.*v-if|v-if.*v-for" src/ --include="*.vue"`
**修正**: 使用 template 包裹或计算属性过滤

```vue
<!-- ❌ 错误 -->
<li v-for="item in items" v-if="item.isActive">

<!-- ✅ 正确 -->
<template v-for="item in items" :key="item.id">
  <li v-if="item.isActive">{{ item.name }}</li>
</template>
```

### ❌ TypeScript: 事件类型隐式 any

**问题**: 事件参数 e 类型推断失败
**检测**: `grep -rE "= \(e\) =>" src/ --include="*.tsx"`
**修正**: 明确声明事件类型

```tsx
// ❌ 错误
const handleChange = (e) => console.log(e.target.value);

// ✅ 正确
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  console.log(e.target.value);
};
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### React 组件模板

```tsx
import { useState, useEffect, useCallback } from 'react';

interface Props {
  id: string;
  onLoad?: (data: Data) => void;
}

export function DataComponent({ id, onLoad }: Props) {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    setLoading(true);
    fetch(`/api/data/${id}`, { signal: controller.signal })
      .then(r => r.json())
      .then(data => {
        setData(data);
        onLoad?.(data);
      })
      .catch(e => {
        if (e.name !== 'AbortError') setError(e);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [id, onLoad]);

  if (loading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;
  if (!data) return <EmptyState />;

  return <DataDisplay data={data} />;
}
```

### Vue 3 组件模板

```vue
<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue';

interface Props {
  id: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  load: [data: Data];
}>();

const data = ref<Data | null>(null);
const loading = ref(true);
const error = ref<Error | null>(null);

let controller: AbortController;

const fetchData = async () => {
  controller = new AbortController();
  loading.value = true;

  try {
    const response = await fetch(`/api/data/${props.id}`, { signal: controller.signal });
    data.value = await response.json();
    emit('load', data.value);
  } catch (e) {
    if ((e as Error).name !== 'AbortError') {
      error.value = e as Error;
    }
  } finally {
    loading.value = false;
  }
};

watch(() => props.id, fetchData, { immediate: true });

onUnmounted(() => controller?.abort());
</script>

<template>
  <Skeleton v-if="loading" />
  <ErrorDisplay v-else-if="error" :error="error" />
  <EmptyState v-else-if="!data" />
  <DataDisplay v-else :data="data" />
</template>
```

### ESLint 配置 (react-hooks)

```json
{
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "error"
  }
}
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前运行

### 自动审计脚本

```bash
#!/bin/bash
# frontend-audit.sh

echo "🔍 Frontend Expert Audit..."

# 1. TypeScript 类型检查
pnpm exec tsc --noEmit || exit 1

# 2. 检查禁止 any
if grep -rE ": any[^a-zA-Z]" src/ --include="*.ts" --include="*.tsx" | grep -v "// TODO"; then
  echo "❌ 发现未注释的 any 类型"
  exit 1
fi

# 3. 检查 console.log
if grep -r "console.log" src/ --include="*.ts" --include="*.tsx"; then
  echo "❌ 发现 console.log"
  exit 1
fi

# 4. 检查 useState 解构丢弃
if grep -rE "const \[,\s*set" src/ --include="*.tsx"; then
  echo "⚠️ 发现 useState 解构丢弃变量，请确认是否需要该变量"
fi

# 5. 检查 key={index}
if grep -rE "key={index}|key=\{i\}" src/ --include="*.tsx"; then
  echo "⚠️ 发现使用 index 作为 key，建议使用唯一 ID"
fi

# 6. ESLint 检查
pnpm lint || exit 1

echo "✅ Frontend Audit Passed"
```

### 交付检查清单

```
□ TypeScript 编译通过（strict 模式）
□ ESLint 零错误零警告（包括 react-hooks/exhaustive-deps）
□ 所有组件覆盖 loading/error/empty 状态
□ useEffect 有清理函数（需要时）
□ 列表渲染使用稳定唯一 key
□ 无 stale closure 问题
□ 移动端测试通过
□ 无控制台错误/警告
```

### 框架特定检查

| 框架 | 检查项 |
|------|--------|
| React | hooks 顺序一致、依赖数组完整、memo 合理使用 |
| Vue | 响应式正确使用、watch 配置正确、v-for 有 key |
| 通用 | 事件类型正确、错误边界、性能优化适度 |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 无泛泛而谈的建议（"小心"、"注意"等）
- [x] 代码块可直接复制使用
