# Component Patterns - 组件模式库

> **组件模式沉淀** | KI 知识自进化系统组件

---

## 📋 模式索引

| 分类 | 模式 | 适用场景 |
|------|------|---------|
| 状态管理 | | |
| 数据获取 | | |
| UI 交互 | | |
| 性能优化 | | |

---

## 🔄 状态管理模式

### Pattern: Redux Slice 标准结构

**适用场景**: 需要创建新的 Redux slice 时

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface XxxState {
  data: XxxType | null;
  loading: boolean;
  error: string | null;
}

const initialState: XxxState = {
  data: null,
  loading: false,
  error: null,
};

export const xxxSlice = createSlice({
  name: 'xxx',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<XxxType>) => {
      state.data = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    reset: () => initialState,
  },
});

export const { setData, setLoading, setError, reset } = xxxSlice.actions;
export default xxxSlice.reducer;
```

**关键点**:
- 始终定义 initialState 类型
- 提供 reset action
- loading/error 状态标准化

---

## 📡 数据获取模式

### Pattern: 异步操作 try-catch 包装

**适用场景**: 所有异步 API 调用

```typescript
async function fetchData(): Promise<Result> {
  try {
    const response = await api.getData();
    return { success: true, data: response };
  } catch (error) {
    console.error('fetchData error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}
```

**关键点**:
- 所有异步操作必须 try-catch
- error 类型安全处理
- 返回统一的 Result 类型

---

## 🎨 UI 交互模式

### Pattern: 三态 UI (Loading/Error/Empty)

**适用场景**: 任何数据展示组件

```tsx
function DataList({ data, loading, error }: Props) {
  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={handleRetry} />;
  }

  if (!data || data.length === 0) {
    return <EmptyState message="暂无数据" />;
  }

  return (
    <ul>
      {data.map(item => <ListItem key={item.id} item={item} />)}
    </ul>
  );
}
```

**关键点**:
- 顺序: loading → error → empty → content
- 每个状态都有对应 UI
- 错误状态提供重试选项

---

## ⚡ 性能优化模式

### Pattern: 虚拟滚动列表

**适用场景**: 列表项 > 100 条

```tsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <ListItem item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

**关键点**:
- 超过 100 项使用虚拟滚动
- 固定行高优先使用 FixedSizeList
- 动态行高使用 VariableSizeList

### Pattern: Memo 优化

**适用场景**: 昂贵计算或频繁渲染

```tsx
// useMemo - 计算结果缓存
const expensiveResult = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// useCallback - 函数引用稳定
const handleClick = useCallback((id: string) => {
  dispatch(selectItem(id));
}, [dispatch]);

// React.memo - 组件级缓存
const MemoizedComponent = React.memo(function Component({ data }: Props) {
  return <div>{data.name}</div>;
});
```

**关键点**:
- 依赖数组必须完整
- 不要过度优化简单组件
- 配合 React DevTools Profiler 验证

---

## 📝 模式记录模板

```markdown
### Pattern: [模式名称]

**适用场景**: [何时使用]

\`\`\`typescript
// 代码示例
\`\`\`

**关键点**:
- 要点 1
- 要点 2

**来源**: [项目/功能名称] | [日期]
```

---

## 🔄 自动触发规则

**何时沉淀**:
1. 发现通用解决方案
2. 重复使用 2+ 次的模式
3. 性能优化技巧
4. 框架最佳实践

**由 ki-manager skill 自动触发评估**
