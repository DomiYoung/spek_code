---
name: lowcode-engine-patterns
description: |
  低代码引擎配置驱动开发最佳实践。当涉及表单配置、列表配置、动态组件时自动触发。
  关键词：lowcode、配置驱动、动态表单、slot、组件工厂、配置化、schema。
  【配置驱动】包含表单生成、列表生成、插槽系统、数据流管理。
allowed-tools: Read, Grep, Glob
---

# 低代码引擎配置驱动开发

## 架构概览

```
配置层 (JSON/Schema)
    ↓
解析层 (ConfigParser)
    ↓
组件工厂 (ComponentFactory)
    ↓
渲染层 (RenderEngine)
    ↓
最终 UI
```

## 表单配置

### 表单 Schema 定义

```javascript
const formConfig = {
  // 表单基础配置
  formProps: {
    labelWidth: '120px',
    labelPosition: 'right',
    size: 'small'
  },

  // 字段配置
  fields: [
    {
      type: 'input',
      field: 'name',
      label: '名称',
      required: true,
      props: {
        placeholder: '请输入名称',
        maxlength: 50,
        showWordLimit: true
      },
      rules: [
        { required: true, message: '请输入名称', trigger: 'blur' }
      ]
    },
    {
      type: 'select',
      field: 'type',
      label: '类型',
      required: true,
      props: {
        placeholder: '请选择类型',
        filterable: true
      },
      options: {
        // 静态选项
        data: [
          { label: '类型A', value: 'A' },
          { label: '类型B', value: 'B' }
        ],
        // 或动态选项
        api: '/api/types',
        labelField: 'name',
        valueField: 'id'
      }
    },
    {
      type: 'date-picker',
      field: 'date',
      label: '日期',
      props: {
        type: 'daterange',
        valueFormat: 'yyyy-MM-dd'
      }
    },
    {
      type: 'number',
      field: 'amount',
      label: '金额',
      props: {
        min: 0,
        precision: 2,
        controlsPosition: 'right'
      }
    },
    {
      type: 'slot',
      field: 'custom',
      label: '自定义',
      slotName: 'customField'
    }
  ],

  // 布局配置
  layout: {
    type: 'grid',
    columns: 2,
    gutter: 20
  },

  // 操作按钮
  actions: {
    submit: { text: '提交', type: 'primary' },
    reset: { text: '重置' },
    cancel: { text: '取消' }
  }
};
```

### 表单渲染组件

```vue
<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="formRules"
    v-bind="config.formProps"
  >
    <el-row :gutter="layout.gutter">
      <el-col
        v-for="field in config.fields"
        :key="field.field"
        :span="24 / layout.columns"
      >
        <el-form-item :label="field.label" :prop="field.field">
          <!-- 动态组件 -->
          <component
            v-if="!field.slotName"
            :is="getComponent(field.type)"
            v-model="formData[field.field]"
            v-bind="field.props"
            :options="getOptions(field)"
          />
          <!-- 插槽 -->
          <slot
            v-else
            :name="field.slotName"
            :field="field"
            :value="formData[field.field]"
            @input="val => formData[field.field] = val"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <!-- 操作按钮 -->
    <el-form-item v-if="config.actions">
      <el-button
        v-if="config.actions.submit"
        :type="config.actions.submit.type"
        @click="handleSubmit"
      >
        {{ config.actions.submit.text }}
      </el-button>
      <el-button
        v-if="config.actions.reset"
        @click="handleReset"
      >
        {{ config.actions.reset.text }}
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
const componentMap = {
  input: 'el-input',
  select: 'el-select',
  number: 'el-input-number',
  'date-picker': 'el-date-picker',
  switch: 'el-switch',
  checkbox: 'el-checkbox-group',
  radio: 'el-radio-group'
};

export default {
  props: {
    config: {
      type: Object,
      required: true
    },
    value: {
      type: Object,
      default: () => ({})
    }
  },

  data() {
    return {
      formData: { ...this.value },
      optionsCache: {}
    };
  },

  computed: {
    formRules() {
      const rules = {};
      this.config.fields.forEach(field => {
        if (field.rules) {
          rules[field.field] = field.rules;
        }
      });
      return rules;
    },

    layout() {
      return this.config.layout || { type: 'grid', columns: 1, gutter: 20 };
    }
  },

  methods: {
    getComponent(type) {
      return componentMap[type] || 'el-input';
    },

    async getOptions(field) {
      if (!field.options) return [];

      // 静态选项
      if (field.options.data) {
        return field.options.data;
      }

      // 动态选项（缓存）
      if (field.options.api) {
        if (!this.optionsCache[field.field]) {
          const response = await this.$http.get(field.options.api);
          this.optionsCache[field.field] = response.data.map(item => ({
            label: item[field.options.labelField],
            value: item[field.options.valueField]
          }));
        }
        return this.optionsCache[field.field];
      }

      return [];
    },

    async handleSubmit() {
      try {
        await this.$refs.formRef.validate();
        this.$emit('submit', this.formData);
      } catch (error) {
        // 验证失败
      }
    },

    handleReset() {
      this.$refs.formRef.resetFields();
      this.$emit('reset');
    }
  }
};
</script>
```

## 列表配置

### 列表 Schema 定义

```javascript
const listConfig = {
  // 表格配置
  tableProps: {
    border: true,
    stripe: true,
    highlightCurrentRow: true
  },

  // 列配置
  columns: [
    {
      type: 'selection',
      width: 55
    },
    {
      type: 'index',
      label: '序号',
      width: 60
    },
    {
      prop: 'name',
      label: '名称',
      minWidth: 150,
      sortable: 'custom',
      showOverflowTooltip: true
    },
    {
      prop: 'status',
      label: '状态',
      width: 100,
      render: 'status-tag',
      renderConfig: {
        mapping: {
          pending: { text: '待处理', type: 'warning' },
          completed: { text: '已完成', type: 'success' }
        }
      }
    },
    {
      prop: 'amount',
      label: '金额',
      width: 120,
      align: 'right',
      formatter: 'money'
    },
    {
      type: 'actions',
      label: '操作',
      width: 180,
      fixed: 'right',
      actions: [
        { key: 'view', text: '查看', permission: 'list:view' },
        { key: 'edit', text: '编辑', permission: 'list:edit' },
        { key: 'delete', text: '删除', type: 'danger', confirm: '确定删除吗？' }
      ]
    }
  ],

  // 数据源
  dataSource: {
    api: '/api/list',
    method: 'post',
    pagination: true,
    pageSize: 20
  },

  // 搜索配置
  searchConfig: {
    fields: [
      { type: 'input', field: 'keyword', label: '关键词' },
      { type: 'select', field: 'status', label: '状态', options: [] }
    ],
    layout: { columns: 4 }
  },

  // 工具栏
  toolbar: {
    buttons: [
      { key: 'add', text: '新增', type: 'primary', icon: 'el-icon-plus' },
      { key: 'export', text: '导出', icon: 'el-icon-download' },
      { key: 'batchDelete', text: '批量删除', type: 'danger', needSelection: true }
    ]
  }
};
```

## 组件工厂

### 工厂模式实现

```javascript
// ComponentFactory.js
class ComponentFactory {
  constructor() {
    this.components = new Map();
    this.renderers = new Map();
    this.formatters = new Map();
  }

  // 注册组件
  registerComponent(type, component) {
    this.components.set(type, component);
  }

  // 注册渲染器
  registerRenderer(name, renderer) {
    this.renderers.set(name, renderer);
  }

  // 注册格式化器
  registerFormatter(name, formatter) {
    this.formatters.set(name, formatter);
  }

  // 获取组件
  getComponent(type) {
    return this.components.get(type) || this.components.get('default');
  }

  // 渲染值
  render(name, value, config) {
    const renderer = this.renderers.get(name);
    return renderer ? renderer(value, config) : value;
  }

  // 格式化值
  format(name, value) {
    const formatter = this.formatters.get(name);
    return formatter ? formatter(value) : value;
  }
}

// 全局实例
export const factory = new ComponentFactory();

// 注册默认格式化器
factory.registerFormatter('money', value => {
  return `￥${Number(value || 0).toFixed(2)}`;
});

factory.registerFormatter('date', value => {
  return value ? moment(value).format('YYYY-MM-DD') : '';
});

factory.registerFormatter('datetime', value => {
  return value ? moment(value).format('YYYY-MM-DD HH:mm:ss') : '';
});

// 注册默认渲染器
factory.registerRenderer('status-tag', (value, config) => {
  const mapping = config.mapping || {};
  const item = mapping[value] || { text: value, type: 'info' };
  return {
    component: 'el-tag',
    props: { type: item.type },
    children: item.text
  };
});
```

## 插槽系统

### 插槽注册表

```javascript
// SlotRegistry.js
class SlotRegistry {
  constructor() {
    this.slots = new Map();
  }

  // 注册插槽
  register(name, config) {
    this.slots.set(name, {
      component: config.component,
      props: config.props || {},
      events: config.events || {}
    });
  }

  // 获取插槽配置
  get(name) {
    return this.slots.get(name);
  }

  // 渲染插槽
  render(name, context) {
    const slot = this.get(name);
    if (!slot) return null;

    return {
      component: slot.component,
      props: {
        ...slot.props,
        ...context
      },
      events: slot.events
    };
  }
}

export const slotRegistry = new SlotRegistry();

// 注册自定义插槽
slotRegistry.register('user-selector', {
  component: () => import('@/components/UserSelector.vue'),
  props: {
    multiple: false
  }
});

slotRegistry.register('file-upload', {
  component: () => import('@/components/FileUpload.vue'),
  props: {
    limit: 5,
    accept: '.jpg,.png,.pdf'
  }
});
```

## 数据流管理

### 统一数据管理器

```javascript
// DataManager.js
class DataManager {
  constructor() {
    this.data = {};
    this.watchers = new Map();
  }

  // 设置数据
  set(key, value) {
    const oldValue = this.data[key];
    this.data[key] = value;

    // 触发监听
    if (this.watchers.has(key)) {
      this.watchers.get(key).forEach(callback => {
        callback(value, oldValue);
      });
    }
  }

  // 获取数据
  get(key) {
    return this.data[key];
  }

  // 监听数据变化
  watch(key, callback) {
    if (!this.watchers.has(key)) {
      this.watchers.set(key, []);
    }
    this.watchers.get(key).push(callback);

    // 返回取消监听函数
    return () => {
      const callbacks = this.watchers.get(key);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    };
  }

  // 批量设置
  setMultiple(data) {
    Object.keys(data).forEach(key => {
      this.set(key, data[key]);
    });
  }

  // 重置
  reset() {
    this.data = {};
  }
}

export const dataManager = new DataManager();
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `vue2-vuex-patterns` | 配置数据状态管理 |
| `element-ui-patterns` | 基础 UI 组件 |
| `ag-grid-patterns` | 复杂表格渲染 |
| `bpmn-workflow-patterns` | 流程表单集成 |

### 关联文件

- `src/utils/lowcode/core/`
- `src/views/commonPage/`
- `src/components/CommonForm/`
- `src/components/CommonList/`
