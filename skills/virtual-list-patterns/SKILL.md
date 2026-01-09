---
name: virtual-list-patterns
description: |
  虚拟列表最佳实践（react-virtuoso、react-window）。当涉及长列表、滚动性能时自动触发。
  关键词：virtuoso、virtual、滚动、列表、性能、react-window、长列表。
  【性能核心】包含虚拟化、动态高度、无限滚动。
allowed-tools: Read, Grep, Glob
---

# 虚拟列表模式

## React Virtuoso（推荐）

### 1. 基础用法

```typescript
import { Virtuoso } from 'react-virtuoso';

function VirtualList({ items }: { items: Item[] }) {
  return (
    <Virtuoso
      style={{ height: '400px' }}
      data={items}
      itemContent={(index, item) => (
        <div className="item">{item.name}</div>
      )}
    />
  );
}
```

### 2. 动态高度

```typescript
// Virtuoso 自动处理动态高度，无需额外配置
<Virtuoso
  data={messages}
  itemContent={(index, message) => (
    <div className="message">
      {message.content}  {/* 高度可变 */}
    </div>
  )}
/>
```

### 3. 无限滚动

```typescript
function InfiniteList() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);

  const loadMore = async () => {
    if (loading) return;
    setLoading(true);
    const newItems = await fetchMoreItems();
    setItems(prev => [...prev, ...newItems]);
    setLoading(false);
  };

  return (
    <Virtuoso
      data={items}
      endReached={loadMore}
      overscan={200}  // 预加载
      itemContent={(index, item) => <ItemComponent item={item} />}
      components={{
        Footer: () => loading ? <Spinner /> : null,
      }}
    />
  );
}
```

### 4. 聊天列表（反向滚动）

```typescript
function ChatList({ messages }: { messages: Message[] }) {
  const virtuosoRef = useRef<VirtuosoHandle>(null);

  // 新消息时滚动到底部
  useEffect(() => {
    virtuosoRef.current?.scrollToIndex({
      index: messages.length - 1,
      behavior: 'smooth',
    });
  }, [messages.length]);

  return (
    <Virtuoso
      ref={virtuosoRef}
      data={messages}
      followOutput="smooth"  // 自动跟踪新消息
      initialTopMostItemIndex={messages.length - 1}  // 从底部开始
      itemContent={(index, message) => (
        <MessageBubble message={message} />
      )}
    />
  );
}
```

## React Window（轻量）

### 固定高度列表

```typescript
import { FixedSizeList } from 'react-window';

function FixedList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: CSSProperties }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList
      height={400}
      width="100%"
      itemCount={items.length}
      itemSize={50}  // 固定行高
    >
      {Row}
    </FixedSizeList>
  );
}
```

### 动态高度列表

```typescript
import { VariableSizeList } from 'react-window';

function VariableList({ items }: { items: Item[] }) {
  const listRef = useRef<VariableSizeList>(null);
  const sizeMap = useRef<Record<number, number>>({});

  const getSize = (index: number) => sizeMap.current[index] || 50;

  const setSize = (index: number, size: number) => {
    sizeMap.current[index] = size;
    listRef.current?.resetAfterIndex(index);
  };

  return (
    <VariableSizeList
      ref={listRef}
      height={400}
      itemCount={items.length}
      itemSize={getSize}
    >
      {({ index, style }) => (
        <AutoSizer onResize={(size) => setSize(index, size.height)}>
          {items[index].content}
        </AutoSizer>
      )}
    </VariableSizeList>
  );
}
```

## 性能优化

```typescript
// 1. 使用 memo 避免重渲染
const ItemComponent = memo(({ item }: { item: Item }) => (
  <div>{item.name}</div>
));

// 2. 设置合适的 overscan
<Virtuoso overscan={200} />  // 预渲染更多项

// 3. 避免内联样式
// ❌ style={{ padding: 10 }}
// ✅ className="item-padding"
```

## 常见陷阱

### ❌ 陷阱 1：容器没有固定高度

```typescript
// ❌ 错误：父容器高度不确定
<div>
  <Virtuoso data={items} />  {/* 不渲染任何内容 */}
</div>

// ✅ 正确：设置固定高度或 flex
<div style={{ height: '100vh' }}>
  <Virtuoso data={items} />
</div>
```

### ❌ 陷阱 2：key 冲突

```typescript
// ❌ 错误：使用 index 作为 key
itemContent={(index) => <Item key={index} />}

// ✅ 正确：使用唯一 ID
itemContent={(index, item) => <Item key={item.id} />}
```

---

**✅ 虚拟列表 Skill 已集成**
