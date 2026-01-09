---
name: mxgraph-patterns
description: |
  MxGraph/DrawIO 底层引擎最佳实践。当涉及图形编辑、单元格操作、编解码时自动触发。
  关键词：mxgraph、mxCell、mxGraph、drawio、图形、编辑器。
  【图形核心】包含单元格操作、事件处理、XML 编解码。
allowed-tools: Read, Grep, Glob
---

# MxGraph 图形引擎模式

## 核心概念

```
mxGraph 结构:
├── mxGraph          # 主图形对象
├── mxGraphModel     # 数据模型
├── mxCell           # 单元格（节点、边）
├── mxGeometry       # 几何信息
└── mxCodec          # XML 编解码
```

## 基础用法

### 1. 初始化

```typescript
import mxgraph from 'mxgraph';

const mx = mxgraph({});
const { mxGraph, mxRubberband, mxEvent } = mx;

function initGraph(container: HTMLElement) {
  // 检查浏览器支持
  if (!mxClient.isBrowserSupported()) {
    return null;
  }

  const graph = new mxGraph(container);

  // 启用框选
  new mxRubberband(graph);

  // 禁用右键菜单
  mxEvent.disableContextMenu(container);

  return graph;
}
```

### 2. 添加单元格

```typescript
const graph = initGraph(container);
const parent = graph.getDefaultParent();

graph.getModel().beginUpdate();
try {
  // 添加节点
  const v1 = graph.insertVertex(
    parent,
    null,           // ID (null = 自动生成)
    '节点 1',       // 标签
    20, 20,         // x, y
    80, 30          // 宽, 高
  );

  const v2 = graph.insertVertex(parent, null, '节点 2', 200, 150, 80, 30);

  // 添加边
  graph.insertEdge(parent, null, '连线', v1, v2);

} finally {
  graph.getModel().endUpdate();
}
```

### 3. 事件处理

```typescript
// 单击事件
graph.addListener(mxEvent.CLICK, (sender, evt) => {
  const cell = evt.getProperty('cell');
  if (cell) {
    console.log('点击:', cell.getValue());
  }
});

// 双击编辑
graph.addListener(mxEvent.DOUBLE_CLICK, (sender, evt) => {
  const cell = evt.getProperty('cell');
  if (cell && cell.isVertex()) {
    graph.startEditingAtCell(cell);
  }
});

// 选择变化
graph.getSelectionModel().addListener(mxEvent.CHANGE, () => {
  const cells = graph.getSelectionCells();
  console.log('选中:', cells);
});
```

### 4. XML 编解码

```typescript
// 导出为 XML
function exportXml(graph: mxGraph): string {
  const encoder = new mxCodec();
  const node = encoder.encode(graph.getModel());
  return mxUtils.getXml(node);
}

// 从 XML 导入
function importXml(graph: mxGraph, xml: string): void {
  const doc = mxUtils.parseXml(xml);
  const codec = new mxCodec(doc);
  codec.decode(doc.documentElement, graph.getModel());
}
```

## 与 react-drawio 集成

```typescript
import { DrawIoEmbed, DrawIoEmbedRef, EventExport } from 'react-drawio';

function DrawIOEditor() {
  const drawioRef = useRef<DrawIoEmbedRef>(null);

  const handleExport = (data: EventExport) => {
    console.log('导出:', data.data);  // Base64 PNG 或 XML
  };

  const handleSave = (data: EventExport) => {
    // 保存到后端
    api.saveDiagram(data.xml);
  };

  return (
    <DrawIoEmbed
      ref={drawioRef}
      urlParameters={{
        ui: 'kennedy',
        spin: true,
        libraries: true,
      }}
      onExport={handleExport}
      onSave={handleSave}
    />
  );
}
```

## 常见陷阱

### ❌ 陷阱 1：忘记 beginUpdate/endUpdate

```typescript
// ❌ 错误：每次操作都触发重绘
graph.insertVertex(...);
graph.insertVertex(...);  // 两次重绘

// ✅ 正确：批量更新
graph.getModel().beginUpdate();
try {
  graph.insertVertex(...);
  graph.insertVertex(...);
} finally {
  graph.getModel().endUpdate();  // 一次重绘
}
```

### ❌ 陷阱 2：模块加载问题

```typescript
// ❌ 错误：直接 import
import { mxGraph } from 'mxgraph';  // 不工作

// ✅ 正确：使用工厂函数
import mxgraph from 'mxgraph';
const mx = mxgraph({});
const { mxGraph } = mx;
```

---

**✅ MxGraph Skill 已集成**
