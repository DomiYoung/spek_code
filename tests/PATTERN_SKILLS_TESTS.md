# Pattern Skills 真实场景测试用例

> **目的**：验证 Pattern Skills 的审计规则是否能检测真实代码问题
> **创建日期**：2026-01-09
> **作者**：Claude + YOUR_USERNAME

---

## 测试用例总览

| ID | Skill | 场景 | 预期结果 |
|----|-------|------|---------
| TC-P01 | signalr-patterns | 未清理事件监听 | 检测并警告 |
| TC-P02 | signalr-patterns | 未检查连接状态 | 检测并警告 |
| TC-P03 | reactflow-patterns | 缺少 parentNode | 检测并拒绝 |
| TC-P04 | reactflow-patterns | 忘记 updateNodeInternals | 检测并警告 |
| TC-P05 | radix-ui-patterns | 缺少 asChild | 检测并警告 |
| TC-P06 | radix-ui-patterns | 缺少 Portal | 检测并警告 |
| TC-P07 | tailwindcss-patterns | 动态类名问题 | 检测并警告 |
| TC-P08 | indexeddb-patterns | 缺少事务错误处理 | 检测并警告 |

---

## TC-P01: SignalR 未清理事件监听

### Skill
`signalr-patterns`

### 场景描述
开发者在 useEffect 中注册 SignalR 事件监听但忘记清理。

### 违规代码
```typescript
// test-patterns/signalr-no-cleanup.tsx
import { useEffect } from 'react';
import { connection } from './signalr';

function ChatMessages() {
  useEffect(() => {
    // ❌ 错误：没有返回清理函数
    connection.on('ReceiveMessage', (msg) => {
      console.log(msg);
    });
  }, []);

  return <div>Messages</div>;
}
```

### 审计命令
```bash
# 检测 SignalR connection.on 但无 connection.off
grep -A20 "connection\.on\(" src/ -r --include="*.tsx" | \
  grep -B10 "useEffect" | \
  grep -L "connection\.off"
```

### 通过标准
- ✅ 检测到缺少 `connection.off` 清理
- ✅ 提供修正建议（添加 cleanup 函数）

### 修正后代码
```typescript
useEffect(() => {
  const handleMessage = (msg) => {
    console.log(msg);
  };

  connection.on('ReceiveMessage', handleMessage);

  return () => {
    connection.off('ReceiveMessage', handleMessage);  // ✅ 清理
  };
}, []);
```

---

## TC-P02: SignalR 未检查连接状态

### Skill
`signalr-patterns`

### 场景描述
发送消息前未检查连接状态，可能导致运行时错误。

### 违规代码
```typescript
// test-patterns/signalr-no-check.ts
async function sendMessage(content: string) {
  // ❌ 错误：未检查连接状态
  await connection.invoke('SendMessage', content);
}
```

### 审计命令
```bash
# 检测 invoke 但未检查 connection.state
grep -B5 "connection\.invoke" src/ -r --include="*.ts" | \
  grep -v "connection\.state" | \
  grep "invoke"
```

### 通过标准
- ✅ 检测到 `invoke` 调用前无状态检查
- ✅ 提供修正建议

---

## TC-P03: ReactFlow 缺少 parentNode

### Skill
`reactflow-patterns`

### 场景描述
创建迭代子节点时忘记设置 parentNode，导致子节点不显示在容器内。

### 违规代码
```typescript
// test-patterns/reactflow-no-parent.ts
const newNode = {
  id: 'child-1',
  type: 'custom',
  position: { x: 50, y: 50 },
  // ❌ 错误：缺少 parentNode
  data: {
    config: {
      isInIteration: true,
      iterationId: 'iteration-1',
    }
  }
};
```

### 审计命令
```bash
# 检测 isInIteration: true 但无 parentNode
grep -A10 "isInIteration.*true" src/ -r --include="*.ts" | \
  grep -B5 -A5 "isInIteration" | \
  grep -v "parentNode"
```

### 通过标准
- ✅ 检测到设置了 `isInIteration` 但缺少 `parentNode`
- ✅ 明确指出 ReactFlow 11.x 使用 `parentNode` 不是 `parentId`

---

## TC-P04: ReactFlow 忘记 updateNodeInternals

### Skill
`reactflow-patterns`

### 场景描述
添加子节点后忘记调用 updateNodeInternals，导致边连接点不更新。

### 违规代码
```typescript
// test-patterns/reactflow-no-update.ts
function addChildNode(iterationId: string) {
  const newNode = createChildNode(iterationId);
  actions.addNode(newNode);
  actions.addEdge(createEdge(newNode.id));
  // ❌ 错误：忘记调用 updateNodeInternals
}
```

### 审计命令
```bash
# 检测添加节点后是否有 updateNodeInternals
grep -A15 "addNode\(" src/ -r --include="*.ts" | \
  grep -B10 "addNode" | \
  grep -v "updateNodeInternals"
```

### 通过标准
- ✅ 检测到 `addNode` 后缺少 `updateNodeInternals`
- ✅ 警告可能导致边连接点不正确

---

## TC-P05: Radix UI 缺少 asChild

### Skill
`radix-ui-patterns`

### 场景描述
Trigger 组件内直接放置子元素但未使用 asChild，导致多余 DOM 节点。

### 违规代码
```typescript
// test-patterns/radix-no-aschild.tsx
import * as Dialog from '@radix-ui/react-dialog';

function MyDialog() {
  return (
    <Dialog.Root>
      {/* ❌ 错误：缺少 asChild */}
      <Dialog.Trigger>
        <button>打开</button>
      </Dialog.Trigger>
    </Dialog.Root>
  );
}
```

### 审计命令
```bash
# 检测 Radix Trigger 内有子元素但无 asChild
grep -A3 "<.*\.Trigger>" src/ -r --include="*.tsx" | \
  grep -v "asChild" | \
  grep "Trigger"
```

### 通过标准
- ✅ 检测到 Trigger 内有子元素但无 `asChild`
- ✅ 警告会产生多余 DOM 节点

---

## TC-P06: Radix UI 缺少 Portal

### Skill
`radix-ui-patterns`

### 场景描述
Dialog/Dropdown Content 未包装在 Portal 中，可能被父容器 overflow 裁剪。

### 违规代码
```typescript
// test-patterns/radix-no-portal.tsx
import * as Dialog from '@radix-ui/react-dialog';

function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button>打开</button>
      </Dialog.Trigger>
      {/* ❌ 错误：Content 未包装在 Portal 中 */}
      <Dialog.Content>
        内容
      </Dialog.Content>
    </Dialog.Root>
  );
}
```

### 审计命令
```bash
# 检测 Dialog.Content 但无 Dialog.Portal
grep -B5 "Dialog\.Content" src/ -r --include="*.tsx" | \
  grep -v "Dialog\.Portal"
```

### 通过标准
- ✅ 检测到 `Dialog.Content` 前无 `Dialog.Portal`
- ✅ 警告可能被 overflow 裁剪

---

## TC-P07: TailwindCSS 动态类名问题

### Skill
`tailwindcss-patterns`

### 场景描述
使用字符串拼接动态生成 Tailwind 类名，被 PurgeCSS 移除。

### 违规代码
```typescript
// test-patterns/tailwind-dynamic-class.tsx
function Button({ color }: { color: string }) {
  // ❌ 错误：动态类名会被 PurgeCSS 移除
  return <button className={`bg-${color}-500`}>Click</button>;
}
```

### 审计命令
```bash
# 检测 Tailwind 类名中的模板字符串
grep -rn "className=.*\`.*\${" src/ --include="*.tsx"
```

### 通过标准
- ✅ 检测到模板字符串内的动态 Tailwind 类名
- ✅ 建议使用 safelist 或预定义映射

### 修正后代码
```typescript
const colorMap = {
  red: 'bg-red-500',
  blue: 'bg-blue-500',
  green: 'bg-green-500',
};

function Button({ color }: { color: keyof typeof colorMap }) {
  return <button className={colorMap[color]}>Click</button>;  // ✅
}
```

---

## TC-P08: IndexedDB 缺少事务错误处理

### Skill
`indexeddb-patterns`

### 场景描述
IndexedDB 事务操作缺少错误处理，可能导致静默失败。

### 违规代码
```typescript
// test-patterns/indexeddb-no-catch.ts
async function saveData(data: any) {
  const db = await openDB('mydb', 1);
  const tx = db.transaction('store', 'readwrite');
  // ❌ 错误：没有 try-catch 和事务错误处理
  await tx.store.put(data);
}
```

### 审计命令
```bash
# 检测 IndexedDB 操作但无 try-catch
grep -A10 "transaction\(" src/ -r --include="*.ts" | \
  grep -B5 "put\|add\|delete" | \
  grep -v "try\|catch"
```

### 通过标准
- ✅ 检测到事务操作无错误处理
- ✅ 建议添加 try-catch 和 `tx.onerror`

---

## 执行方法

### 创建测试文件

```bash
#!/bin/bash
mkdir -p /tmp/test-patterns

# TC-P01: SignalR 无清理
cat > /tmp/test-patterns/signalr-no-cleanup.tsx << 'EOF'
import { useEffect } from 'react';
import { connection } from './signalr';

function ChatMessages() {
  useEffect(() => {
    connection.on('ReceiveMessage', (msg) => {
      console.log(msg);
    });
  }, []);
  return <div>Messages</div>;
}
EOF

# TC-P05: Radix 无 asChild
cat > /tmp/test-patterns/radix-no-aschild.tsx << 'EOF'
import * as Dialog from '@radix-ui/react-dialog';

function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <button>打开</button>
      </Dialog.Trigger>
    </Dialog.Root>
  );
}
EOF

# TC-P07: Tailwind 动态类名
cat > /tmp/test-patterns/tailwind-dynamic-class.tsx << 'EOF'
function Button({ color }: { color: string }) {
  return <button className={`bg-${color}-500`}>Click</button>;
}
EOF
```

### 运行测试

```bash
# TC-P01 测试
echo "TC-P01: SignalR 事件监听清理检测"
if grep -q "connection\.on" /tmp/test-patterns/signalr-no-cleanup.tsx && \
   ! grep -q "connection\.off" /tmp/test-patterns/signalr-no-cleanup.tsx; then
  echo "✅ PASS - 检测到未清理的事件监听"
else
  echo "❌ FAIL"
fi

# TC-P05 测试
echo "TC-P05: Radix asChild 检测"
if grep -q "Dialog\.Trigger>" /tmp/test-patterns/radix-no-aschild.tsx && \
   ! grep -q "asChild" /tmp/test-patterns/radix-no-aschild.tsx; then
  echo "✅ PASS - 检测到缺少 asChild"
else
  echo "❌ FAIL"
fi

# TC-P07 测试
echo "TC-P07: Tailwind 动态类名检测"
if grep -qE 'className=.*`.*\$\{' /tmp/test-patterns/tailwind-dynamic-class.tsx; then
  echo "✅ PASS - 检测到动态 Tailwind 类名"
else
  echo "❌ FAIL"
fi
```

---

## 验收标准

| 测试 | 通过条件 |
|------|---------
| TC-P01 | 检测到 `connection.on` 无对应 `connection.off` |
| TC-P02 | 检测到 `invoke` 前无 `connection.state` 检查 |
| TC-P03 | 检测到 `isInIteration: true` 无 `parentNode` |
| TC-P04 | 检测到 `addNode` 后无 `updateNodeInternals` |
| TC-P05 | 检测到 `Trigger` 内有子元素无 `asChild` |
| TC-P06 | 检测到 `Content` 无 `Portal` 包装 |
| TC-P07 | 检测到 `className` 内模板字符串动态类名 |
| TC-P08 | 检测到事务操作无 `try-catch` |

---

**Created**: 2026-01-09
**Purpose**: 验证 Pattern Skills 审计规则有效性
