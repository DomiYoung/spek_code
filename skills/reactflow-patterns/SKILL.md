---
name: reactflow-patterns
description: |
  ReactFlow 11.x 工作流编辑器专业知识。当涉及节点、边、Handle、迭代节点、画布操作、节点持久化时自动触发。
  包含迭代节点、子节点持久化、parentNode、expandParent 等关键业务知识。
  触发关键词：ReactFlow、节点、边、Handle、parentNode、迭代、workflow、画布、连接、updateNodeInternals。
allowed-tools: Read, Grep, Glob, Task
---

# ReactFlow 11.x 工作流开发指南

> **技术版本**: ReactFlow 11.x | React 18+ | TypeScript 5+
> **核心理念**: 节点即组件，边即关系，状态即真相

---

## Quick Reference（快速查阅）

### 节点属性速查表

| 属性 | 类型 | 用途 | 示例 |
|------|------|------|------|
| `id` | `string` | 唯一标识 | `"node-1"` |
| `type` | `string` | 节点类型 | `"custom"`, `"default"` |
| `position` | `{x, y}` | 位置坐标 | `{ x: 100, y: 50 }` |
| `data` | `object` | 自定义数据 | `{ label: "节点" }` |
| `parentNode` | `string` | 父节点 ID（11.x） | `"iteration-1"` |
| `expandParent` | `boolean` | 自动扩展父节点 | `true` |
| `draggable` | `boolean` | 可拖拽 | `true` |
| `selectable` | `boolean` | 可选中 | `true` |
| `hidden` | `boolean` | 隐藏 | `false` |

### 边属性速查表

| 属性 | 类型 | 用途 | 示例 |
|------|------|------|------|
| `id` | `string` | 唯一标识 | `"edge-1"` |
| `source` | `string` | 源节点 ID | `"node-1"` |
| `target` | `string` | 目标节点 ID | `"node-2"` |
| `sourceHandle` | `string` | 源连接点 | `"output-0"` |
| `targetHandle` | `string` | 目标连接点 | `"input-0"` |
| `type` | `string` | 边类型 | `"smoothstep"` |
| `animated` | `boolean` | 动画 | `true` |

### Handle 属性速查表

| 属性 | 类型 | 用途 | 示例 |
|------|------|------|------|
| `type` | `"source" \| "target"` | 连接类型 | `"source"` |
| `position` | `Position` | 位置 | `Position.Right` |
| `id` | `string` | 连接点 ID | `"output-0"` |
| `isConnectable` | `boolean` | 可连接 | `true` |

### 常用 Hooks

| Hook | 用途 | 返回值 |
|------|------|--------|
| `useNodes()` | 获取所有节点 | `Node[]` |
| `useEdges()` | 获取所有边 | `Edge[]` |
| `useReactFlow()` | 获取实例方法 | `ReactFlowInstance` |
| `useNodeId()` | 获取当前节点 ID | `string` |
| `useStore()` | 访问内部 store | `StoreApi` |
| `useUpdateNodeInternals()` | 更新节点内部 | `(nodeId) => void` |

---

## 项目架构

```
src/features/workflow-editor/
├── canvas/
│   └── hooks/
│       ├── useNodesInteractions.ts  # 节点交互
│       └── useEdgesInteractions.ts  # 边交互
├── components/
│   ├── CustomNode.tsx               # 自定义节点
│   ├── IterationElement/            # 迭代节点 ⚠️ 重点
│   │   ├── IterationNode.tsx        # 迭代容器
│   │   └── AddBlock.tsx             # 添加子节点
│   └── edges/                       # 自定义边
├── hooks/
│   ├── useIterationChildren.ts      # 迭代子节点管理
│   └── useWorkflowPersistence.ts    # 持久化
├── state/
│   └── workflowStore.ts             # Zustand 状态
└── utils/
    ├── workflowCache.ts             # IndexedDB 缓存
    └── iterationHelpers.ts          # 迭代辅助函数
```

---

## 1. 硬性约束 (Hard Constraints)

### 迭代节点约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 子节点必须设置 parentNode | `isInIteration: true` 必须有 `parentNode` | `grep -A10 "isInIteration.*true" src/ --include="*.ts" \| grep -v "parentNode"` | 🔴 Critical |
| 使用 parentNode 不是 parentId | ReactFlow 11.x 使用 parentNode | `grep -rn "parentId" src/ --include="*.ts" \| grep -v "// legacy"` | 🔴 Critical |
| 必须设置 expandParent | 子节点必须有 `expandParent: true` | `grep -B5 -A5 "parentNode" src/ --include="*.ts" \| grep -v "expandParent"` | 🟡 Warning |
| 添加节点后必须 updateNodeInternals | 否则 Handle 位置不更新 | `grep -A15 "addNode" src/ --include="*.ts" \| grep -v "updateNodeInternals"` | 🔴 Critical |

### 状态管理约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 禁止直接修改 nodes/edges | 必须通过 store action | `grep -rn "setNodes\|setEdges" src/components/ --include="*.tsx"` | 🟡 Warning |
| 必须使用 immer 更新 | 复杂更新使用 immer | `grep -rn "produce\|immer" src/state/ --include="*.ts"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 缺少 parentNode

**问题**：创建迭代子节点时忘记设置 parentNode，导致子节点不显示在容器内。

**检测**：
```bash
# 检测 isInIteration: true 但无 parentNode
grep -A10 "isInIteration.*true" src/ -r --include="*.ts" | \
  grep -B5 -A5 "isInIteration" | \
  grep -v "parentNode"

# 检测使用了废弃的 parentId
grep -rn "parentId:" src/ --include="*.ts" | grep -v "// legacy\|// deprecated"
```

**修正**：
```typescript
// ❌ 错误：缺少 parentNode
const newNode = {
  id: 'child-1',
  type: 'custom',
  position: { x: 50, y: 50 },
  data: {
    config: {
      isInIteration: true,
      iterationId: 'iteration-1',
    }
  }
};

// ✅ 正确：设置 parentNode（ReactFlow 11.x）
const newNode = {
  id: 'child-1',
  type: 'custom',
  position: { x: 50, y: 50 },  // 相对于父节点的位置
  parentNode: 'iteration-1',   // ⚠️ ReactFlow 11.x 使用 parentNode
  expandParent: true,          // ⚠️ 必须设置
  data: {
    config: {
      isInIteration: true,
      iterationId: 'iteration-1',
    }
  }
};
```

---

### 反模式 2.2: 忘记 updateNodeInternals

**问题**：添加子节点后忘记调用 updateNodeInternals，导致边连接点不更新。

**检测**：
```bash
# 检测添加节点后是否有 updateNodeInternals
grep -A15 "addNode\(" src/ -r --include="*.ts" | \
  grep -B10 "addNode" | \
  grep -v "updateNodeInternals"
```

**修正**：
```typescript
// ❌ 错误：忘记调用 updateNodeInternals
function addChildNode(iterationId: string) {
  const newNode = createChildNode(iterationId);
  actions.addNode(newNode);
  actions.addEdge(createEdge(newNode.id));
  // 缺少 updateNodeInternals
}

// ✅ 正确：调用 updateNodeInternals
function addChildNode(iterationId: string) {
  const newNode = createChildNode(iterationId);
  actions.addNode(newNode);
  actions.addEdge(createEdge(newNode.id));

  // ⚠️ 关键：同步 ReactFlow 内部状态
  updateNodeInternals(iterationId);
}
```

---

### 反模式 2.3: 双重标识不同步

**问题**：ReactFlow 的 `parentNode` 和业务层的 `relation_id` 不同步，导致刷新后子节点丢失。

**检测**：
```bash
# 检测添加第一个子节点时是否更新 relation_id
grep -A20 "addNode\|addChildNode" src/ -r --include="*.ts" | \
  grep -v "relation_id"
```

**修正**：
```typescript
// ❌ 错误：只设置 parentNode，不更新 relation_id
actions.addNode(newNode);

// ✅ 正确：同时更新两层
// 1. ReactFlow 层
actions.addNode(newNode);

// 2. 业务层（仅第一个子节点）
if (childCount === 0) {
  actions.updateNode(iterationNodeId, {
    config: {
      relation_id: Number(newNodeId)  // 第一个子节点作为入口
    }
  });
}

// 3. 同步内部状态
updateNodeInternals(iterationNodeId);
```

---

### 反模式 2.4: 节点组件不使用 memo

**问题**：自定义节点组件未使用 React.memo，导致不必要的重渲染。

**检测**：
```bash
# 检测节点组件是否使用 memo
grep -rn "export.*function.*Node\|export.*const.*Node" src/components/ --include="*.tsx" | \
  xargs -I {} sh -c 'grep -L "React.memo\|memo(" {}'
```

**修正**：
```typescript
// ❌ 错误：未使用 memo
export function CustomNode({ data }: NodeProps<CustomNodeData>) {
  return <div>{data.label}</div>;
}

// ✅ 正确：使用 memo
export const CustomNode = React.memo(({ data }: NodeProps<CustomNodeData>) => {
  return <div>{data.label}</div>;
});
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 双重标识机制

```
┌─────────────────────────────────────────────────────────────┐
│ ReactFlow 层（运行时显示）                                   │
│                                                              │
│ • parentNode: 视觉分组，子节点相对于父节点定位               │
│ • 用于画布渲染和交互                                         │
│ • 存储在 node.parentNode                                     │
│ • ReactFlow 11.x 使用 parentNode（不是 parentId）            │
└─────────────────────────────────────────────────────────────┘
                              ↕ 需要同步
┌─────────────────────────────────────────────────────────────┐
│ 业务层（持久化和恢复）                                       │
│                                                              │
│ • relation_id: 迭代节点的入口子节点 ID                       │
│ • 用于后端存储和刷新后恢复                                   │
│ • 存储在 node.data.config.relation_id                        │
│ • 配合 edges 通过 DFS 遍历找到所有子节点                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 添加子节点的正确方式

```typescript
// AddBlock.tsx - 添加子节点的正确实现

function addChildNode(iterationNodeId: string) {
  const newNodeId = `child-${Date.now()}`;
  const childCount = getChildCount(iterationNodeId);

  // 1. 创建节点，设置 parentNode（ReactFlow 层）
  const newNode: Node = {
    id: newNodeId,
    type: 'custom',
    position: calculateChildPosition(childCount),
    parentNode: iterationNodeId,  // ⚠️ ReactFlow 11.x
    expandParent: true,
    data: {
      config: {
        isInIteration: true,
        iterationId: iterationNodeId,
      }
    }
  };

  // 2. 添加到 store
  actions.addNode(newNode);

  // 3. 🔥 关键：更新迭代节点的 relation_id（业务层）
  if (childCount === 0) {
    actions.updateNode(iterationNodeId, {
      config: {
        relation_id: Number(newNodeId)  // 第一个子节点作为入口
      }
    });
  }

  // 4. 同步 ReactFlow 内部状态
  updateNodeInternals(iterationNodeId);
}
```

### 3.3 节点组件优化

```typescript
// 使用 React.memo 和 useCallback 优化
export const CustomNode = React.memo(({ data, id }: NodeProps<CustomNodeData>) => {
  const updateNode = useStore(state => state.updateNode);

  // 使用 useCallback 避免重新创建函数
  const handleClick = useCallback(() => {
    updateNode(id, { selected: true });
  }, [id, updateNode]);

  return (
    <div className="custom-node" onClick={handleClick}>
      <Handle type="source" position={Position.Right} />
      <span>{data.label}</span>
      <Handle type="target" position={Position.Left} />
    </div>
  );
});
```

### 3.4 持久化恢复流程

```typescript
// 恢复时重建 parentNode 关系
function restoreIterationChildren(
  nodes: Node[],
  edges: Edge[],
  iterationNode: Node
) {
  const relationId = iterationNode.data?.config?.relation_id;
  if (!relationId) return nodes;

  // 通过 DFS 从 relation_id 开始遍历
  const childIds = findChildrenByDFS(edges, String(relationId));

  return nodes.map(node => {
    if (childIds.includes(node.id)) {
      return {
        ...node,
        parentNode: iterationNode.id,  // 恢复 parentNode
        expandParent: true,
      };
    }
    return node;
  });
}
```

---

## 4. 自我验证 (Self-Verification)

### ReactFlow 合规审计脚本

```bash
#!/bin/bash
# reactflow-audit.sh - ReactFlow 代码合规检查

echo "🔄 ReactFlow 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测缺少 parentNode
echo -e "\n📍 检测 parentNode 设置..."
MISSING_PARENT=$(grep -A10 "isInIteration.*true" src/ -r --include="*.ts" 2>/dev/null | \
  grep -B5 -A5 "isInIteration" | grep -c "parentNode" || echo "0")

if [ "$MISSING_PARENT" -eq 0 ]; then
    echo "⚠️ 可能缺少 parentNode 设置"
    echo "   检查 isInIteration: true 的节点"
else
    echo "✅ parentNode 设置正常"
fi

# 2. 检测使用废弃的 parentId
echo -e "\n🔍 检测废弃 API..."
PARENT_ID=$(grep -rn "parentId:" src/ --include="*.ts" 2>/dev/null | grep -v "// legacy\|// deprecated" | head -5)

if [ -n "$PARENT_ID" ]; then
    echo "❌ 发现废弃的 parentId（应使用 parentNode）:"
    echo "$PARENT_ID"
    ((ERRORS++))
else
    echo "✅ 未使用废弃 API"
fi

# 3. 检测 updateNodeInternals
echo -e "\n🔄 检测 updateNodeInternals..."
ADD_NODE_COUNT=$(grep -rn "addNode\(" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')
UPDATE_INTERNALS=$(grep -rn "updateNodeInternals" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$ADD_NODE_COUNT" -gt 0 ] && [ "$UPDATE_INTERNALS" -eq 0 ]; then
    echo "⚠️ 有 addNode 调用但无 updateNodeInternals"
    echo "   添加节点后可能需要调用 updateNodeInternals"
else
    echo "✅ updateNodeInternals 使用正常"
fi

# 4. 检测节点组件 memo
echo -e "\n⚡ 检测节点组件优化..."
NODE_COMPONENTS=$(grep -rln "NodeProps\|: FC.*Node" src/components/ --include="*.tsx" 2>/dev/null)
UNMEMOIZED=""

for file in $NODE_COMPONENTS; do
    if ! grep -q "React.memo\|memo(" "$file" 2>/dev/null; then
        UNMEMOIZED="$UNMEMOIZED\n  - $file"
    fi
done

if [ -n "$UNMEMOIZED" ]; then
    echo "⚠️ 以下节点组件未使用 memo:$UNMEMOIZED"
else
    echo "✅ 节点组件已优化"
fi

# 5. 检测 relation_id 同步
echo -e "\n🔗 检测双重标识同步..."
RELATION_ID=$(grep -rn "relation_id" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$RELATION_ID" -eq 0 ]; then
    echo "⚠️ 未发现 relation_id 使用"
    echo "   持久化可能不完整"
else
    echo "✅ relation_id 已配置"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ ReactFlow 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 子节点设置了 `parentNode`（不是 parentId）
- [ ] 子节点设置了 `expandParent: true`
- [ ] 添加节点后调用了 `updateNodeInternals`
- [ ] 第一个子节点更新了 `relation_id`
- [ ] 节点组件使用了 `React.memo`
- [ ] 事件处理器使用了 `useCallback`

---

## 5. Common Mistakes（常见错误速查）

> 借鉴 makepad-skills 的 ✅/❌ 对照格式，快速识别和修复问题。

### 5.1 节点创建

```typescript
// ❌ WRONG - 使用废弃的 parentId（ReactFlow 10.x）
const node = {
  id: 'child-1',
  parentId: 'parent-1',  // Error: parentId is deprecated in 11.x
};

// ✅ CORRECT - 使用 parentNode（ReactFlow 11.x）
const node = {
  id: 'child-1',
  parentNode: 'parent-1',  // Correct for ReactFlow 11.x
  expandParent: true,      // Always set this
};
```

### 5.2 Handle 更新

```typescript
// ❌ WRONG - 添加节点后不更新 Handle
actions.addNode(newNode);
actions.addEdge(newEdge);
// Handle 位置不会更新，连线可能错位

// ✅ CORRECT - 使用 updateNodeInternals
actions.addNode(newNode);
actions.addEdge(newEdge);
updateNodeInternals(parentNodeId);  // 同步 Handle 位置
```

### 5.3 节点组件

```typescript
// ❌ WRONG - 未使用 memo，每次父组件更新都重渲染
export function CustomNode({ data }: NodeProps) {
  return <div>{data.label}</div>;
}

// ✅ CORRECT - 使用 memo 优化性能
export const CustomNode = memo(({ data }: NodeProps) => {
  return <div>{data.label}</div>;
});
```

### 5.4 事件处理

```typescript
// ❌ WRONG - 每次渲染创建新函数
const CustomNode = memo(({ id }) => {
  const handleClick = () => updateNode(id);  // 每次渲染新引用
  return <div onClick={handleClick} />;
});

// ✅ CORRECT - 使用 useCallback 稳定引用
const CustomNode = memo(({ id }) => {
  const handleClick = useCallback(() => updateNode(id), [id]);
  return <div onClick={handleClick} />;
});
```

### 5.5 状态访问

```typescript
// ❌ WRONG - 订阅整个 store，任何变化都触发重渲染
const { nodes, edges, settings } = useStore();

// ✅ CORRECT - 使用 selector 精确订阅
const nodes = useStore(state => state.nodes);
const getNode = useStore(state => state.getNode);
```

### 错误速查表

| 错误 | 原因 | 修复 |
|------|------|------|
| 子节点不在容器内显示 | 缺少 `parentNode` | 添加 `parentNode: parentId` |
| 刷新后子节点丢失 | 未设置 `relation_id` | 第一个子节点更新 `relation_id` |
| 连线错位 | 未调用 `updateNodeInternals` | 添加节点后调用 |
| 节点频繁重渲染 | 未使用 `memo` | 用 `memo` 包裹组件 |
| Handle 位置错误 | `parentId` vs `parentNode` | 使用 `parentNode`（11.x） |
| 拖拽后位置不保存 | 未监听 `onNodesChange` | 处理位置变化事件 |

---

## 6. Complete Examples（完整示例）

### 6.1 自定义节点完整模板

```typescript
import { memo, useCallback } from 'react';
import { Handle, Position, NodeProps, useReactFlow } from 'reactflow';

interface CustomNodeData {
  label: string;
  config: {
    isInIteration?: boolean;
    iterationId?: string;
  };
}

export const CustomNode = memo(({ id, data, selected }: NodeProps<CustomNodeData>) => {
  const { updateNodeData } = useReactFlow();

  const handleLabelChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    updateNodeData(id, { label: e.target.value });
  }, [id, updateNodeData]);

  return (
    <div className={`custom-node ${selected ? 'selected' : ''}`}>
      {/* 输入 Handle */}
      <Handle
        type="target"
        position={Position.Left}
        id="input-0"
        isConnectable={true}
      />

      {/* 节点内容 */}
      <div className="node-header">
        <input
          value={data.label}
          onChange={handleLabelChange}
          className="node-label-input"
        />
      </div>

      {/* 输出 Handle */}
      <Handle
        type="source"
        position={Position.Right}
        id="output-0"
        isConnectable={true}
      />
    </div>
  );
});

CustomNode.displayName = 'CustomNode';
```

### 6.2 迭代节点添加子节点

```typescript
import { useReactFlow, useUpdateNodeInternals } from 'reactflow';
import { useWorkflowStore } from '../state/workflowStore';

export function useAddIterationChild() {
  const { getNodes } = useReactFlow();
  const updateNodeInternals = useUpdateNodeInternals();
  const { addNode, updateNode } = useWorkflowStore();

  return useCallback((iterationId: string) => {
    const nodes = getNodes();
    const iterationNode = nodes.find(n => n.id === iterationId);
    if (!iterationNode) return;

    // 计算子节点数量
    const childCount = nodes.filter(
      n => n.parentNode === iterationId
    ).length;

    // 生成新节点 ID
    const newNodeId = `child-${Date.now()}`;

    // 1️⃣ 创建子节点（设置 parentNode）
    const newNode = {
      id: newNodeId,
      type: 'custom',
      position: {
        x: 50 + childCount * 200,  // 相对于父节点
        y: 100,
      },
      parentNode: iterationId,     // ⚠️ ReactFlow 11.x
      expandParent: true,          // ⚠️ 必须设置
      data: {
        label: `步骤 ${childCount + 1}`,
        config: {
          isInIteration: true,
          iterationId,
        },
      },
    };

    addNode(newNode);

    // 2️⃣ 更新 relation_id（第一个子节点）
    if (childCount === 0) {
      updateNode(iterationId, {
        config: {
          ...iterationNode.data.config,
          relation_id: Number(newNodeId),
        },
      });
    }

    // 3️⃣ 同步 ReactFlow 内部状态
    requestAnimationFrame(() => {
      updateNodeInternals(iterationId);
    });

    return newNodeId;
  }, [getNodes, addNode, updateNode, updateNodeInternals]);
}
```

### 6.3 节点注册

```typescript
// nodeTypes.ts - 注册所有节点类型
import { CustomNode } from './CustomNode';
import { IterationNode } from './IterationNode';
import { StartNode } from './StartNode';
import { EndNode } from './EndNode';

// ⚠️ 必须在组件外定义，避免重新创建
export const nodeTypes = {
  custom: CustomNode,
  iteration: IterationNode,
  start: StartNode,
  end: EndNode,
} as const;

// 使用
<ReactFlow
  nodes={nodes}
  edges={edges}
  nodeTypes={nodeTypes}  // 传入节点类型映射
  // ...
/>
```

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `zustand-patterns` | 节点状态存储在 Zustand store |
| `indexeddb-patterns` | 工作流持久化到 IndexedDB |
| `code-quality-gates` | 检查 memo 使用、性能优化 |

### 关联文件

- `src/features/workflow-editor/**/*.ts`
- `src/features/workflow-editor/components/**/*.tsx`

---

**✅ ReactFlow Patterns v2.0.0** | **标准 4 Section 已集成** | **专家路由保留**
