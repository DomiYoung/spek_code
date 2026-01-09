---
name: ag-grid-patterns
description: |
  AG-Grid Enterprise 企业级表格最佳实践。当涉及大数据表格、复杂表格、单元格渲染时自动触发。
  关键词：ag-grid、gridOptions、columnDefs、cellRenderer、rowData、enterprise、表格。
  【高性能表格】包含列配置、单元格渲染、筛选排序、性能优化、企业功能。
version: 2.0.0
allowed-tools: Read, Grep, Glob
---

# AG-Grid Enterprise 企业级表格

## 项目架构

```
src/components/
├── CommonTable/
│   └── AgGridTable.vue      # AG-Grid 封装组件
├── renderers/               # 自定义渲染器
│   ├── StatusRenderer.js
│   └── ActionRenderer.js
└── mixins/
    └── agGridMixin.js       # 通用 AG-Grid 混入

技术栈：
- AG-Grid Enterprise 30.x
- Vue 2.x / Vue 3.x / React
```

---

## 1. 硬性约束 (Hard Constraints)

### 配置约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 增量更新必须配置 getRowId | deltaRowDataMode 需要 | `grep -rn "deltaRowDataMode\\|immutableData" src/ --include="*.vue" \| xargs grep -L "getRowId\\|getRowNodeId"` | 🔴 Critical |
| 销毁时必须调用 destroy() | 防止内存泄漏 | `grep -rln "AgGridVue\\|ag-grid-react" src/ --include="*.vue" --include="*.tsx" \| xargs grep -L "destroy()"` | 🔴 Critical |
| 禁止列定义中直接使用 this | 上下文可能丢失 | `grep -rn "columnDefs.*this\\." src/ --include="*.vue" --include="*.js"` | 🔴 Critical |
| 必须配置 defaultColDef | 避免重复列配置 | `grep -rln "columnDefs" src/ --include="*.vue" \| xargs grep -L "defaultColDef"` | 🟡 Warning |

### 性能约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| >1000 行必须启用虚拟化 | 保持滚动流畅 | `grep -rn "suppressRowVirtualisation.*true" src/ --include="*.vue"` | 🔴 Critical |
| 禁止直接修改 rowData | 必须使用 API 更新 | `grep -rn "this\\.rowData\\[.*\\]\\s*=" src/ --include="*.vue"` | 🔴 Critical |
| 服务端模式必须处理 fail | 错误处理不能缺失 | `grep -A20 "getRows.*async" src/ --include="*.js" \| grep -v "failCallback\\|params.fail"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 直接修改 rowData

**问题**：直接修改数组元素，AG-Grid 无法检测变化，UI 不更新。

**检测**：
```bash
# 检测直接数组修改
grep -rn "this\.rowData\[.*\]\s*=" src/ --include="*.vue" --include="*.js"

# 检测 push/splice 等直接操作
grep -rn "rowData\.\(push\|splice\|pop\|shift\)" src/ --include="*.vue"
```

**修正**：
```javascript
// ❌ 错误：直接修改（UI 不更新）
this.rowData[0].name = 'New Name';
this.rowData.push(newItem);

// ✅ 正确：使用 Transaction API
this.gridApi.applyTransaction({
  update: [{ ...this.rowData[0], name: 'New Name' }]
});

this.gridApi.applyTransaction({
  add: [newItem],
  addIndex: 0  // 插入位置
});

// ✅ 正确：刷新特定单元格
this.gridApi.refreshCells({
  rowNodes: [rowNode],
  columns: ['name'],
  force: true
});
```

---

### 反模式 2.2: 列定义中使用 this

**问题**：valueFormatter/cellRenderer 中的 this 在运行时可能丢失，导致方法调用失败。

**检测**：
```bash
# 检测列定义中的 this 引用
grep -rn "valueFormatter.*this\." src/ --include="*.vue" --include="*.js"
grep -rn "cellRenderer.*this\." src/ --include="*.vue" --include="*.js"
grep -rn "valueGetter.*this\." src/ --include="*.vue" --include="*.js"
```

**修正**：
```javascript
// ❌ 错误：this 可能丢失
columnDefs: [
  {
    field: 'date',
    valueFormatter: params => this.formatDate(params.value)  // 💥 this undefined
  }
]

// ✅ 正确：使用 context 传递
gridOptions: {
  context: { componentParent: this }
},
columnDefs: [
  {
    field: 'date',
    valueFormatter: params => {
      const parent = params.context.componentParent;
      return parent.formatDate(params.value);
    }
  }
]

// ✅ 正确：使用独立工具函数
import { formatDate } from '@/utils/date';
columnDefs: [
  {
    field: 'date',
    valueFormatter: params => formatDate(params.value)
  }
]
```

---

### 反模式 2.3: 忘记销毁 gridApi

**问题**：组件销毁时未调用 destroy()，导致事件监听器和定时器残留，内存泄漏。

**检测**：
```bash
# 检测使用 AG-Grid 但无 destroy 调用
grep -rln "gridApi\s*=" src/ --include="*.vue" | \
  xargs grep -L "destroy()"

# 检测 beforeDestroy/unmounted 中是否清理
grep -A10 "beforeDestroy\|beforeUnmount\|unmounted" src/ --include="*.vue" | \
  grep -v "gridApi.*destroy\|destroy()"
```

**修正**：
```javascript
// ❌ 错误：未清理资源
beforeDestroy() {
  // 什么都没做
}

// ✅ 正确：完整清理
beforeDestroy() {
  if (this.gridApi) {
    this.gridApi.destroy();
    this.gridApi = null;
    this.columnApi = null;
  }
}

// ✅ Vue 3 Composition API
onBeforeUnmount(() => {
  gridApi.value?.destroy();
  gridApi.value = null;
});
```

---

### 反模式 2.4: 服务端模式未处理错误

**问题**：getRows 中只处理成功，忽略 failCallback，导致加载状态卡死。

**检测**：
```bash
# 检测 getRows 实现是否有错误处理
grep -A20 "getRows.*params" src/ --include="*.js" --include="*.vue" | \
  grep -B15 "successCallback\|params.success" | \
  grep -v "failCallback\|params.fail\|catch"
```

**修正**：
```javascript
// ❌ 错误：无错误处理
getRows: async (params) => {
  const data = await api.getList(params);
  params.successCallback(data.rows, data.total);
  // 如果 api.getList 失败，表格卡在加载状态
}

// ✅ 正确：完整错误处理
getRows: async (params) => {
  try {
    const data = await api.getList({
      startRow: params.startRow,
      endRow: params.endRow,
      sortModel: params.sortModel,
      filterModel: params.filterModel
    });
    params.successCallback(data.rows, data.total);
  } catch (error) {
    console.error('AG-Grid data fetch failed:', error);
    params.failCallback();  // ⚠️ 必须调用！
    // 可选：显示错误提示
    this.$message.error('数据加载失败');
  }
}
```

---

### 反模式 2.5: 大数据禁用虚拟化

**问题**：数据量大时禁用虚拟化，导致 DOM 节点过多，滚动卡顿。

**检测**：
```bash
# 检测禁用虚拟化的配置
grep -rn "suppressRowVirtualisation.*true" src/ --include="*.vue" --include="*.js"
grep -rn "suppressColumnVirtualisation.*true" src/ --include="*.vue" --include="*.js"

# 检测大数据量但未优化
grep -rn "rowData.*length\s*>" src/ --include="*.vue" | grep -v "rowBuffer"
```

**修正**：
```javascript
// ❌ 错误：禁用虚拟化
gridOptions: {
  suppressRowVirtualisation: true,  // 💥 大数据会卡死
  suppressColumnVirtualisation: true
}

// ✅ 正确：启用虚拟化 + 优化配置
gridOptions: {
  // 保持虚拟化开启（默认）
  suppressRowVirtualisation: false,
  suppressColumnVirtualisation: false,

  // 行缓冲优化
  rowBuffer: 10,  // 可视区域外缓冲行数

  // 大数据优化
  animateRows: false,  // 关闭动画
  suppressCellSelection: true,  // 减少重绘

  // 增量更新模式
  immutableData: true,
  getRowId: params => params.data.id
}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 基础配置模板

```vue
<template>
  <ag-grid-vue
    class="ag-theme-alpine"
    :style="{ height: tableHeight + 'px', width: '100%' }"
    :gridOptions="gridOptions"
    :columnDefs="columnDefs"
    :rowData="rowData"
    :defaultColDef="defaultColDef"
    :modules="modules"
    @grid-ready="onGridReady"
    @selection-changed="onSelectionChanged"
  />
</template>

<script>
import { AgGridVue } from 'ag-grid-vue';
import { AllModules } from 'ag-grid-enterprise';

export default {
  components: { AgGridVue },

  data() {
    return {
      modules: AllModules,
      gridApi: null,
      columnApi: null,
      tableHeight: 600,

      gridOptions: {
        // 行配置
        rowHeight: 40,
        headerHeight: 44,
        rowSelection: 'multiple',
        suppressRowClickSelection: true,

        // 性能优化
        animateRows: true,
        rowBuffer: 10,

        // 增量更新
        immutableData: true,
        getRowId: params => params.data.id,

        // 上下文传递
        context: { componentParent: this },

        // 分页
        pagination: true,
        paginationPageSize: 50
      },

      defaultColDef: {
        flex: 1,
        minWidth: 100,
        resizable: true,
        sortable: true,
        filter: true
      },

      columnDefs: [],
      rowData: []
    };
  },

  methods: {
    onGridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
    },

    onSelectionChanged() {
      const selected = this.gridApi.getSelectedRows();
      this.$emit('selection-change', selected);
    }
  },

  beforeDestroy() {
    if (this.gridApi) {
      this.gridApi.destroy();
      this.gridApi = null;
      this.columnApi = null;
    }
  }
};
</script>
```

### 3.2 自定义单元格渲染器

```javascript
// StatusRenderer.js - 使用 context 安全访问父组件
export default {
  template: `
    <span :class="['status-tag', statusClass]">
      {{ statusText }}
    </span>
  `,

  computed: {
    statusMap() {
      // 从 context 获取配置（安全）
      return this.params.context.componentParent.statusConfig || {
        pending: { text: '待处理', class: 'warning' },
        completed: { text: '已完成', class: 'success' },
        failed: { text: '失败', class: 'danger' }
      };
    },
    statusText() {
      return this.statusMap[this.params.value]?.text || this.params.value;
    },
    statusClass() {
      return this.statusMap[this.params.value]?.class || '';
    }
  }
};

// 注册渲染器
gridOptions: {
  components: {
    statusRenderer: StatusRenderer
  },
  context: {
    componentParent: this,
    statusConfig: { /* 自定义配置 */ }
  }
}
```

### 3.3 服务端分页模式

```javascript
gridOptions: {
  rowModelType: 'serverSide',
  serverSideStoreType: 'partial',
  cacheBlockSize: 100
},

methods: {
  onGridReady(params) {
    const datasource = {
      getRows: async (params) => {
        const request = params.request;

        try {
          const response = await api.getServerData({
            startRow: request.startRow,
            endRow: request.endRow,
            sortModel: request.sortModel,
            filterModel: request.filterModel
          });

          params.success({
            rowData: response.data,
            rowCount: response.total
          });
        } catch (error) {
          console.error('Server data fetch failed:', error);
          params.fail();  // ⚠️ 必须调用
          this.$message.error('加载失败，请重试');
        }
      }
    };

    params.api.setServerSideDatasource(datasource);
  },

  // 刷新服务端数据
  refreshServerData() {
    this.gridApi.refreshServerSide({ purge: true });
  }
}
```

### 3.4 Transaction API 数据更新

```javascript
// 增删改查最佳实践
const gridDataService = {
  // 添加行
  addRows(gridApi, newRows, index = 0) {
    gridApi.applyTransaction({
      add: newRows,
      addIndex: index
    });
  },

  // 更新行
  updateRows(gridApi, updatedRows) {
    gridApi.applyTransaction({
      update: updatedRows
    });
  },

  // 删除行
  removeRows(gridApi, rowsToRemove) {
    gridApi.applyTransaction({
      remove: rowsToRemove
    });
  },

  // 批量操作
  batchUpdate(gridApi, { add = [], update = [], remove = [] }) {
    gridApi.applyTransaction({ add, update, remove });
  },

  // 刷新特定单元格
  refreshCells(gridApi, rowNodes, columns) {
    gridApi.refreshCells({
      rowNodes,
      columns,
      force: true
    });
  }
};
```

### 3.5 企业功能：行分组与聚合

```javascript
columnDefs: [
  {
    headerName: '地区',
    field: 'region',
    rowGroup: true,
    hide: true
  },
  {
    headerName: '城市',
    field: 'city',
    rowGroup: true,
    hide: true
  },
  {
    headerName: '销售额',
    field: 'sales',
    aggFunc: 'sum',
    valueFormatter: params => `￥${params.value?.toFixed(2)}`
  }
],

gridOptions: {
  groupDefaultExpanded: 1,
  autoGroupColumnDef: {
    headerName: '分组',
    minWidth: 200,
    cellRendererParams: {
      suppressCount: false
    }
  }
}
```

---

## 4. 自我验证 (Self-Verification)

### AG-Grid 合规审计脚本

```bash
#!/bin/bash
# ag-grid-audit.sh - AG-Grid 代码合规检查

echo "📊 AG-Grid 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测直接修改 rowData
echo -e "\n📦 检测数据更新方式..."
DIRECT_MODIFY=$(grep -rn "this\.rowData\[.*\]\s*=" src/ --include="*.vue" --include="*.js" 2>/dev/null | wc -l | tr -d ' ')

if [ "$DIRECT_MODIFY" -gt 0 ]; then
    echo "❌ 发现直接修改 rowData（应使用 applyTransaction）:"
    grep -rn "this\.rowData\[.*\]\s*=" src/ --include="*.vue" --include="*.js" 2>/dev/null | head -5
    ((ERRORS++))
else
    echo "✅ 数据更新方式正确"
fi

# 2. 检测列定义中的 this 引用
echo -e "\n🔗 检测 this 上下文..."
THIS_IN_COLS=$(grep -rn "valueFormatter.*this\.\|cellRenderer.*this\." src/ --include="*.vue" --include="*.js" 2>/dev/null | wc -l | tr -d ' ')

if [ "$THIS_IN_COLS" -gt 0 ]; then
    echo "❌ 列定义中使用 this（应使用 context）:"
    grep -rn "valueFormatter.*this\.\|cellRenderer.*this\." src/ --include="*.vue" --include="*.js" 2>/dev/null | head -5
    ((ERRORS++))
else
    echo "✅ 上下文使用正确"
fi

# 3. 检测 destroy 调用
echo -e "\n🧹 检测资源清理..."
GRID_FILES=$(grep -rln "gridApi\s*=" src/ --include="*.vue" 2>/dev/null)
MISSING_DESTROY=""

for file in $GRID_FILES; do
    if ! grep -q "destroy()" "$file" 2>/dev/null; then
        MISSING_DESTROY="$MISSING_DESTROY\n  - $file"
    fi
done

if [ -n "$MISSING_DESTROY" ]; then
    echo "❌ 以下文件缺少 destroy() 调用:$MISSING_DESTROY"
    ((ERRORS++))
else
    echo "✅ 资源清理正确"
fi

# 4. 检测 defaultColDef 配置
echo -e "\n⚙️ 检测默认列配置..."
COLS_FILES=$(grep -rln "columnDefs" src/ --include="*.vue" 2>/dev/null)
MISSING_DEFAULT=""

for file in $COLS_FILES; do
    if ! grep -q "defaultColDef" "$file" 2>/dev/null; then
        MISSING_DEFAULT="$MISSING_DEFAULT\n  - $file"
    fi
done

if [ -n "$MISSING_DEFAULT" ]; then
    echo "⚠️ 以下文件缺少 defaultColDef:$MISSING_DEFAULT"
else
    echo "✅ 默认列配置正确"
fi

# 5. 检测禁用虚拟化
echo -e "\n⚡ 检测虚拟化配置..."
VIRT_DISABLED=$(grep -rn "suppressRowVirtualisation.*true" src/ --include="*.vue" --include="*.js" 2>/dev/null | wc -l | tr -d ' ')

if [ "$VIRT_DISABLED" -gt 0 ]; then
    echo "⚠️ 发现禁用虚拟化（大数据可能卡顿）:"
    grep -rn "suppressRowVirtualisation.*true" src/ --include="*.vue" --include="*.js" 2>/dev/null
else
    echo "✅ 虚拟化配置正确"
fi

# 6. 检测服务端错误处理
echo -e "\n🌐 检测服务端错误处理..."
SERVER_MODE=$(grep -rln "rowModelType.*serverSide\|rowModelType.*infinite" src/ --include="*.vue" --include="*.js" 2>/dev/null)
MISSING_FAIL=""

for file in $SERVER_MODE; do
    if ! grep -q "failCallback\|params\.fail" "$file" 2>/dev/null; then
        MISSING_FAIL="$MISSING_FAIL\n  - $file"
    fi
done

if [ -n "$MISSING_FAIL" ]; then
    echo "❌ 服务端模式缺少错误处理:$MISSING_FAIL"
    ((ERRORS++))
else
    if [ -n "$SERVER_MODE" ]; then
        echo "✅ 服务端错误处理正确"
    else
        echo "ℹ️ 未使用服务端模式"
    fi
fi

# 7. 检测 getRowId 配置
echo -e "\n🆔 检测增量更新配置..."
IMMUTABLE=$(grep -rln "immutableData.*true\|deltaRowDataMode" src/ --include="*.vue" --include="*.js" 2>/dev/null)
MISSING_ID=""

for file in $IMMUTABLE; do
    if ! grep -q "getRowId\|getRowNodeId" "$file" 2>/dev/null; then
        MISSING_ID="$MISSING_ID\n  - $file"
    fi
done

if [ -n "$MISSING_ID" ]; then
    echo "❌ 增量模式缺少 getRowId:$MISSING_ID"
    ((ERRORS++))
else
    if [ -n "$IMMUTABLE" ]; then
        echo "✅ 增量更新配置正确"
    else
        echo "ℹ️ 未使用增量更新模式"
    fi
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ AG-Grid 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 使用 `applyTransaction` 更新数据，不直接修改 rowData
- [ ] 列定义使用 `context` 传递父组件引用
- [ ] `beforeDestroy` 中调用 `gridApi.destroy()`
- [ ] 配置了 `defaultColDef` 避免重复配置
- [ ] 大数据保持虚拟化开启
- [ ] 服务端模式处理了 `failCallback`
- [ ] 增量更新模式配置了 `getRowId`

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `virtual-list-patterns` | 超大数据替代方案 |
| `react-query-patterns` | 数据获取和缓存 |
| `zustand-patterns` | 表格状态管理 |
| `lowcode-engine-patterns` | 配置驱动表格生成 |

### 关联文件

- `src/components/CommonTable/AgGridTable.vue`
- `src/mixins/agGridMixin.js`
- `src/utils/gridDataService.js`

---

**✅ AG-Grid Patterns v2.0.0** | **标准 4 Section 已集成**
