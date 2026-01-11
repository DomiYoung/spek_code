---
name: zustand-patterns
description: |
  Zustand 4.x 状态管理专家 - store 设计、性能优化。
  Use when:
  - 创建/修改 store、状态管理
  - 使用 immer、shallow、devtools
  - 解决状态订阅、重渲染问题
  触发词：Zustand、store、状态、immer、shallow、useStore、全局状态
  Related Skills: reactflow-patterns, react-query-patterns, indexeddb-patterns
allowed-tools: Read, Grep, Glob
---

# Zustand 4.x 状态管理专家

> **核心理念**：最小化重渲染，actions 分离，immer 安全修改。
> **来源**：[Zustand 官方文档](https://docs.pmnd.rs/zustand)、[React 状态管理最佳实践](https://react.dev/)

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **禁止整体订阅** | 不允许 `useStore()` 无 selector | `grep -rE "use\w+Store\(\s*\)" src/ --include="*.tsx"` |
| **必须使用 shallow** | 多字段选择必须 shallow 比较 | `grep -rE "=>\s*\(\{" src/ --include="*.tsx" \| grep -v "shallow"` |
| **禁止 immer 返回值** | immer 中不返回新对象 | `grep -rE "set\(\(state\)\s*=>\s*\{[^}]*return" src/` |
| **Actions 分离** | actions 必须在 store 内定义 | 代码审查：检查 actions 对象存在 |
| **Store 拆分** | 单 store < 10 个状态字段 | 代码审查：检查 interface 字段数 |
| **类型完整** | Store 必须有 TypeScript 类型 | `grep -rE "create\(\)\(" src/ \| grep -v "<\w+>"` |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 订阅整个 Store 导致性能问题 ⭐⭐⭐⭐⭐

**问题**: 任何状态变化都触发组件重渲染，性能急剧下降
**检测**: `grep -rE "const \w+ = use\w+Store\(\s*\)" src/ --include="*.tsx"`
**修正**: 使用 selector 订阅特定状态

```typescript
// ❌ 错误 - 任何变化都重渲染
const store = useWorkflowStore();
return <div>{store.nodes.length}</div>;

// ✅ 正确 - 只订阅需要的状态
const nodes = useWorkflowStore((state) => state.nodes);
return <div>{nodes.length}</div>;
```

### ❌ 多字段选择未使用 shallow ⭐⭐⭐⭐⭐

**问题**: 每次渲染创建新对象，导致无限重渲染
**检测**: `grep -rE "=>\s*\(\{\s*\w+:" src/ --include="*.tsx" | grep -v "shallow"`
**修正**: 添加 shallow 比较器

```typescript
// ❌ 错误 - 每次都是新对象引用
const { nodes, edges } = useWorkflowStore((state) => ({
  nodes: state.nodes,
  edges: state.edges,
}));  // 无限重渲染！

// ✅ 正确 - 使用 shallow 比较
import { shallow } from 'zustand/shallow';

const { nodes, edges } = useWorkflowStore(
  (state) => ({ nodes: state.nodes, edges: state.edges }),
  shallow
);
```

### ❌ immer 中返回新对象 ⭐⭐⭐⭐

**问题**: 破坏 immer 代理机制，状态更新可能失效
**检测**: `grep -rE "set\(\(state\)\s*=>\s*\{[^}]*return\s*\{" src/`
**修正**: 直接修改 state 或使用 set({})

```typescript
// ❌ 错误 - immer 中返回新对象
set((state) => {
  return { ...state, nodes: [...state.nodes, node] };  // 破坏 immer！
});

// ✅ 正确 - 直接修改
set((state) => {
  state.nodes.push(node);  // immer 允许直接修改
});

// ✅ 也正确 - 不使用 immer 参数
set({ nodes: [...get().nodes, node] });
```

### ❌ selector 中进行复杂计算 ⭐⭐⭐⭐

**问题**: 每次渲染都重新计算，性能差
**检测**: `grep -rE "useStore\([^)]*\.filter\(|\.map\(|\.reduce\(" src/`
**修正**: 使用 useMemo 缓存计算结果

```typescript
// ❌ 错误 - 每次渲染都重新 filter
const filteredNodes = useStore((state) =>
  state.nodes.filter(n => n.type === 'custom')
);

// ✅ 正确 - 分离选择和计算
const nodes = useStore((state) => state.nodes);
const filteredNodes = useMemo(
  () => nodes.filter(n => n.type === 'custom'),
  [nodes]
);
```

### ❌ 异步操作未处理错误状态 ⭐⭐⭐

**问题**: 加载失败无反馈，用户体验差
**检测**: `grep -rE "async.*=>\s*\{" src/stores/ | grep -v "catch\|error"`
**修正**: 统一 loading/error 状态管理

```typescript
// ❌ 错误 - 无错误处理
fetchData: async () => {
  const data = await api.getData();
  set({ data });
}

// ✅ 正确 - 完整的状态管理
fetchData: async () => {
  set({ isLoading: true, error: null });
  try {
    const data = await api.getData();
    set({ data, isLoading: false });
  } catch (error) {
    set({
      error: error instanceof Error ? error : new Error('Unknown'),
      isLoading: false
    });
  }
}
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### Store 定义模板（使用 Immer + DevTools）

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { devtools } from 'zustand/middleware';

interface WorkflowState {
  // 状态
  nodes: Node[];
  edges: Edge[];
  isLoading: boolean;
  error: Error | null;
}

interface WorkflowActions {
  addNode: (node: Node) => void;
  updateNode: (id: string, data: Partial<NodeData>) => void;
  removeNode: (id: string) => void;
  fetchWorkflow: (id: string) => Promise<void>;
}

interface WorkflowStore extends WorkflowState {
  actions: WorkflowActions;
}

export const useWorkflowStore = create<WorkflowStore>()(
  devtools(
    immer((set, get) => ({
      // 初始状态
      nodes: [],
      edges: [],
      isLoading: false,
      error: null,

      // Actions 分组
      actions: {
        addNode: (node) => set((state) => {
          state.nodes.push(node);
        }),

        updateNode: (id, data) => set((state) => {
          const node = state.nodes.find(n => n.id === id);
          if (node) {
            Object.assign(node.data, data);
          }
        }),

        removeNode: (id) => set((state) => {
          state.nodes = state.nodes.filter(n => n.id !== id);
        }),

        fetchWorkflow: async (id) => {
          set({ isLoading: true, error: null });
          try {
            const data = await api.getWorkflow(id);
            set((state) => {
              state.nodes = data.nodes;
              state.edges = data.edges;
              state.isLoading = false;
            });
          } catch (error) {
            set({
              error: error instanceof Error ? error : new Error('Unknown'),
              isLoading: false,
            });
          }
        },
      },
    })),
    { name: 'WorkflowStore' }
  )
);
```

### 组件中使用模板

```typescript
import { shallow } from 'zustand/shallow';

function WorkflowEditor() {
  // ✅ 分别订阅状态和 actions
  const { nodes, edges, isLoading, error } = useWorkflowStore(
    (state) => ({
      nodes: state.nodes,
      edges: state.edges,
      isLoading: state.isLoading,
      error: state.error,
    }),
    shallow
  );

  // ✅ Actions 引用稳定，不会触发重渲染
  const { addNode, updateNode } = useWorkflowStore((state) => state.actions);

  // 处理状态
  if (isLoading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;

  return <ReactFlow nodes={nodes} edges={edges} />;
}
```

### 组件外使用模板

```typescript
// 在工具函数、事件处理中使用
export function handleNodeDrop(node: Node) {
  // 获取当前状态（非响应式）
  const { nodes } = useWorkflowStore.getState();

  // 调用 action
  useWorkflowStore.getState().actions.addNode(node);
}

// 订阅状态变化（用于副作用）
const unsubscribe = useWorkflowStore.subscribe(
  (state) => state.nodes,
  (nodes, prevNodes) => {
    if (nodes.length !== prevNodes.length) {
      console.log('Nodes count changed:', nodes.length);
    }
  }
);
```

### Store 拆分策略

```
src/stores/
├── user.ts          # 用户状态 (auth, profile)
├── settings.ts      # 应用设置 (theme, locale)
└── notifications.ts # 通知状态

src/features/
├── workflow-editor/state/
│   └── workflowStore.ts    # 工作流编辑状态
├── chat/state/
│   └── chatStore.ts        # 聊天状态
└── dashboard/state/
    └── dashboardStore.ts   # 仪表盘状态
```

**拆分原则**：
- 按业务领域拆分，非按技术分层
- 单 Store 状态字段 ≤ 10 个
- 高频更新状态独立 Store

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前运行

### 自动审计脚本

```bash
#!/bin/bash
# zustand-audit.sh

echo "🔍 Zustand Expert Audit..."

# 1. 检查整体订阅
FULL_SUB=$(grep -rE "const \w+ = use\w+Store\(\s*\)" src/ --include="*.tsx" 2>/dev/null)
if [ -n "$FULL_SUB" ]; then
  echo "❌ 发现整体订阅 Store（无 selector）:"
  echo "$FULL_SUB"
  exit 1
fi

# 2. 检查多字段选择缺少 shallow
MULTI_SELECT=$(grep -rE "=>\s*\(\{" src/ --include="*.tsx" 2>/dev/null | grep -v "shallow")
if [ -n "$MULTI_SELECT" ]; then
  echo "⚠️ 多字段选择可能缺少 shallow:"
  echo "$MULTI_SELECT"
fi

# 3. 检查 immer 中返回对象
IMMER_RETURN=$(grep -rE "set\(\(state\)\s*=>\s*\{[^}]*return\s*\{" src/ 2>/dev/null)
if [ -n "$IMMER_RETURN" ]; then
  echo "❌ 发现 immer 中返回新对象:"
  echo "$IMMER_RETURN"
  exit 1
fi

# 4. 检查 selector 中复杂计算
SELECTOR_CALC=$(grep -rE "useStore\([^)]*\.(filter|map|reduce)\(" src/ 2>/dev/null)
if [ -n "$SELECTOR_CALC" ]; then
  echo "⚠️ selector 中有复杂计算，建议使用 useMemo:"
  echo "$SELECTOR_CALC"
fi

# 5. 检查 Store 类型定义
UNTYPED=$(grep -rE "create\(\)\(" src/stores/ 2>/dev/null | grep -v "<\w+>")
if [ -n "$UNTYPED" ]; then
  echo "❌ 发现未类型化的 Store:"
  echo "$UNTYPED"
  exit 1
fi

echo "✅ Zustand Audit Passed"
```

### 交付检查清单

```
□ Store 使用 TypeScript 类型定义
□ 使用 immer 中间件处理复杂状态
□ 开发环境启用 devtools 中间件
□ 组件只订阅需要的状态（有 selector）
□ 多字段选择使用 shallow 比较
□ Actions 集中在 store 内定义
□ 异步操作处理 loading/error 状态
□ 大 Store 按领域拆分（≤ 10 字段）
□ selector 中无复杂计算（用 useMemo）
□ 无整体订阅（useStore() 无参数）
```

### 项目架构检查

| 检查项 | 期望 |
|--------|------|
| 全局 Store 位置 | `src/stores/*.ts` |
| 功能 Store 位置 | `src/features/*/state/*.ts` |
| 单 Store 字段数 | ≤ 10 |
| immer 中间件 | 复杂状态必须使用 |
| devtools 中间件 | 开发环境启用 |

---

## 🔗 与全局 Skills 协作

### 触发路径

```
用户: "优化状态管理" / "添加 store" / "zustand"
        ↓
workflow-orchestrator → expert-router
        ↓
本 Skill 提供 Zustand 最佳实践
```

### 协作关系

| Skill | 协作方式 |
|-------|----------|
| `reactflow-patterns` | 配合处理 workflowStore |
| `react-query-patterns` | 区分客户端/服务端状态 |
| `code-quality-gates` | 检查 immer 用法正确性 |
| `frontend-expert` | 提供 React 性能优化指导 |

### 关联文件

- `src/stores/*.ts`
- `src/features/*/state/*.ts`

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 无泛泛而谈的建议（"小心"、"注意"等）
- [x] 代码块可直接复制使用
