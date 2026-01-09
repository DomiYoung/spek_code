---
name: bpmn-workflow-patterns
description: |
  BPMN-JS 流程建模最佳实践。当涉及工作流设计、流程图、审批流程时自动触发。
  关键词：bpmn、workflow、流程图、审批流、diagram、modeler、流程设计。
  【流程建模】包含流程设计器、节点配置、流程执行、属性面板。
allowed-tools: Read, Grep, Glob
---

# BPMN-JS 流程建模

## 基础集成

### Vue 2 集成

```vue
<template>
  <div class="bpmn-container">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-button-group>
        <el-button icon="el-icon-folder-opened" @click="openFile">打开</el-button>
        <el-button icon="el-icon-download" @click="saveBpmn">保存</el-button>
        <el-button icon="el-icon-picture" @click="exportSvg">导出SVG</el-button>
      </el-button-group>
      <el-button-group>
        <el-button icon="el-icon-zoom-in" @click="zoomIn">放大</el-button>
        <el-button icon="el-icon-zoom-out" @click="zoomOut">缩小</el-button>
        <el-button icon="el-icon-rank" @click="fitViewport">适应</el-button>
      </el-button-group>
      <el-button-group>
        <el-button icon="el-icon-refresh-left" @click="undo">撤销</el-button>
        <el-button icon="el-icon-refresh-right" @click="redo">重做</el-button>
      </el-button-group>
    </div>

    <!-- 画布 -->
    <div ref="canvas" class="canvas" />

    <!-- 属性面板 -->
    <div ref="propertiesPanel" class="properties-panel" />

    <!-- 小地图 -->
    <div ref="minimap" class="minimap" />
  </div>
</template>

<script>
import BpmnModeler from 'bpmn-js/lib/Modeler';
import minimapModule from 'diagram-js-minimap';
import {
  BpmnPropertiesPanelModule,
  BpmnPropertiesProviderModule
} from 'bpmn-js-properties-panel';

import 'bpmn-js/dist/assets/diagram-js.css';
import 'bpmn-js/dist/assets/bpmn-font/css/bpmn.css';
import 'bpmn-js-properties-panel/dist/assets/bpmn-js-properties-panel.css';
import 'diagram-js-minimap/assets/diagram-js-minimap.css';

export default {
  data() {
    return {
      modeler: null,
      currentScale: 1
    };
  },

  mounted() {
    this.initModeler();
  },

  beforeDestroy() {
    if (this.modeler) {
      this.modeler.destroy();
    }
  },

  methods: {
    initModeler() {
      this.modeler = new BpmnModeler({
        container: this.$refs.canvas,
        propertiesPanel: {
          parent: this.$refs.propertiesPanel
        },
        additionalModules: [
          minimapModule,
          BpmnPropertiesPanelModule,
          BpmnPropertiesProviderModule
        ],
        minimap: {
          open: true
        }
      });

      // 监听事件
      this.bindEvents();

      // 加载初始流程
      this.loadDiagram();
    },

    bindEvents() {
      const eventBus = this.modeler.get('eventBus');

      // 元素变化
      eventBus.on('element.changed', ({ element }) => {
        console.log('Element changed:', element);
        this.$emit('element-changed', element);
      });

      // 选择变化
      eventBus.on('selection.changed', ({ newSelection }) => {
        this.$emit('selection-changed', newSelection);
      });

      // 画布变化
      eventBus.on('commandStack.changed', () => {
        this.$emit('diagram-changed');
      });
    },

    async loadDiagram(xml) {
      const defaultXml = xml || this.getDefaultDiagram();
      try {
        await this.modeler.importXML(defaultXml);
        this.fitViewport();
      } catch (error) {
        console.error('加载流程失败:', error);
        this.$message.error('加载流程失败');
      }
    },

    getDefaultDiagram() {
      return `<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
          xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
          xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
          id="Definitions_1"
          targetNamespace="http://bpmn.io/schema/bpmn">
          <bpmn:process id="Process_1" isExecutable="true">
            <bpmn:startEvent id="StartEvent_1" name="开始"/>
          </bpmn:process>
          <bpmndi:BPMNDiagram id="BPMNDiagram_1">
            <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">
              <bpmndi:BPMNShape id="_BPMNShape_StartEvent_1" bpmnElement="StartEvent_1">
                <dc:Bounds x="180" y="160" width="36" height="36"/>
              </bpmndi:BPMNShape>
            </bpmndi:BPMNPlane>
          </bpmndi:BPMNDiagram>
        </bpmn:definitions>`;
    },

    // 保存 BPMN
    async saveBpmn() {
      try {
        const { xml } = await this.modeler.saveXML({ format: true });
        this.$emit('save', xml);
        return xml;
      } catch (error) {
        console.error('保存失败:', error);
        throw error;
      }
    },

    // 导出 SVG
    async exportSvg() {
      try {
        const { svg } = await this.modeler.saveSVG();
        const blob = new Blob([svg], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `diagram_${Date.now()}.svg`;
        a.click();
        URL.revokeObjectURL(url);
      } catch (error) {
        console.error('导出失败:', error);
      }
    },

    // 缩放控制
    zoomIn() {
      this.currentScale = Math.min(this.currentScale + 0.1, 3);
      this.modeler.get('canvas').zoom(this.currentScale);
    },

    zoomOut() {
      this.currentScale = Math.max(this.currentScale - 0.1, 0.3);
      this.modeler.get('canvas').zoom(this.currentScale);
    },

    fitViewport() {
      this.modeler.get('canvas').zoom('fit-viewport');
      this.currentScale = 1;
    },

    // 撤销/重做
    undo() {
      this.modeler.get('commandStack').undo();
    },

    redo() {
      this.modeler.get('commandStack').redo();
    }
  }
};
</script>

<style lang="scss" scoped>
.bpmn-container {
  display: flex;
  flex-direction: column;
  height: 100%;

  .toolbar {
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }

  .canvas {
    flex: 1;
    position: relative;
  }

  .properties-panel {
    position: absolute;
    right: 0;
    top: 50px;
    width: 300px;
    height: calc(100% - 50px);
    overflow: auto;
    border-left: 1px solid #ddd;
    background: #fff;
  }

  .minimap {
    position: absolute;
    left: 10px;
    bottom: 10px;
  }
}
</style>
```

## 自定义元素

### 自定义渲染器

```javascript
// customRenderer.js
import BaseRenderer from 'diagram-js/lib/draw/BaseRenderer';
import { is } from 'bpmn-js/lib/util/ModelUtil';

const HIGH_PRIORITY = 1500;

export default class CustomRenderer extends BaseRenderer {
  constructor(eventBus, bpmnRenderer) {
    super(eventBus, HIGH_PRIORITY);
    this.bpmnRenderer = bpmnRenderer;
  }

  canRender(element) {
    return is(element, 'bpmn:Task') && element.businessObject.get('custom:type');
  }

  drawShape(parentNode, element) {
    const shape = this.bpmnRenderer.drawShape(parentNode, element);
    const customType = element.businessObject.get('custom:type');

    // 自定义样式
    if (customType === 'approval') {
      shape.style.fill = '#e6f7ff';
      shape.style.stroke = '#1890ff';
    }

    return shape;
  }
}

CustomRenderer.$inject = ['eventBus', 'bpmnRenderer'];
```

### 自定义面板

```javascript
// customPropertiesProvider.js
import { is } from 'bpmn-js/lib/util/ModelUtil';

export default function CustomPropertiesProvider(propertiesPanel, translate) {
  this.getGroups = function(element) {
    return function(groups) {
      if (is(element, 'bpmn:UserTask')) {
        groups.push({
          id: 'custom',
          label: '自定义属性',
          entries: [
            {
              id: 'assignee',
              component: AssigneeField,
              isEdited: () => true
            },
            {
              id: 'dueDate',
              component: DueDateField,
              isEdited: () => true
            }
          ]
        });
      }
      return groups;
    };
  };
}

CustomPropertiesProvider.$inject = ['propertiesPanel', 'translate'];
```

## 流程模拟

### Token 模拟

```javascript
import TokenSimulationModule from 'bpmn-js-token-simulation';

// 添加模块
additionalModules: [
  TokenSimulationModule
]

// 控制模拟
methods: {
  startSimulation() {
    const tokenSimulation = this.modeler.get('tokenSimulation');
    tokenSimulation.toggleMode();
  },

  pauseSimulation() {
    const tokenSimulation = this.modeler.get('tokenSimulation');
    tokenSimulation.pause();
  },

  resetSimulation() {
    const tokenSimulation = this.modeler.get('tokenSimulation');
    tokenSimulation.resetSimulation();
  }
}
```

## 流程验证

```javascript
import lintModule from 'bpmn-js-bpmnlint';
import bpmnlintConfig from './.bpmnlintrc';

// 添加校验模块
additionalModules: [
  lintModule
],

linting: {
  bpmnlint: bpmnlintConfig
}

// 手动校验
methods: {
  async validateDiagram() {
    const linting = this.modeler.get('linting');
    await linting.toggle(true);

    const issues = linting.getLintErrors();
    if (issues.length > 0) {
      this.$message.warning(`发现 ${issues.length} 个问题`);
    }
    return issues;
  }
}
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `vue2-vuex-patterns` | 流程状态管理 |
| `element-ui-patterns` | 属性面板 UI |
| `lowcode-engine-patterns` | 表单与流程结合 |

### 关联文件

- `src/components/DiagramManager/`
- `src/views/workflow/`
- `node_modules/bpmn-js/`
