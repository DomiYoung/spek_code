# ECharts 代码示例详解

> 📖 **本文件**: 包含 Vue/React 封装、常用图表配置、响应式、主题定制
> **主文件**: [SKILL.md](./SKILL.md)

---

## 1. Vue 2 基础封装

```vue
<template>
  <div ref="chartRef" :style="{ width: width, height: height }" />
</template>

<script>
import * as echarts from 'echarts';
import { debounce } from 'lodash';

export default {
  name: 'EChart',

  props: {
    option: { type: Object, required: true },
    width: { type: String, default: '100%' },
    height: { type: String, default: '400px' },
    theme: { type: String, default: '' },
    autoResize: { type: Boolean, default: true }
  },

  data() {
    return { chart: null, resizeHandler: null };
  },

  watch: {
    option: {
      handler(newOption) { this.setOption(newOption); },
      deep: true
    }
  },

  mounted() {
    this.$nextTick(() => { this.initChart(); });
    if (this.autoResize) {
      this.resizeHandler = debounce(() => { this.chart?.resize(); }, 100);
      window.addEventListener('resize', this.resizeHandler);
    }
  },

  beforeDestroy() {
    if (this.chart) { this.chart.dispose(); this.chart = null; }
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler);
    }
  },

  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chartRef, this.theme);
      this.setOption(this.option);
      this.bindEvents();
    },
    setOption(option) {
      if (this.chart && option) { this.chart.setOption(option, true); }
    },
    bindEvents() {
      this.chart.on('click', params => { this.$emit('chart-click', params); });
      this.chart.on('legendselectchanged', params => { this.$emit('legend-change', params); });
    },
    resize() { this.chart?.resize(); },
    getInstance() { return this.chart; },
    showLoading() { this.chart?.showLoading(); },
    hideLoading() { this.chart?.hideLoading(); }
  }
};
</script>
```

---

## 2. 常用图表配置

### 折线图

```javascript
const lineOption = {
  title: { text: '销售趋势', left: 'center' },
  tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
  legend: { data: ['销售额', '订单量'], bottom: 10 },
  grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: [
    { type: 'value', name: '销售额(万)', position: 'left' },
    { type: 'value', name: '订单量', position: 'right' }
  ],
  series: [
    {
      name: '销售额', type: 'line', smooth: true,
      yAxisIndex: 0, areaStyle: { opacity: 0.3 },
      data: [150, 230, 224, 218, 135, 147]
    },
    {
      name: '订单量', type: 'line', smooth: true,
      yAxisIndex: 1, data: [320, 332, 301, 334, 390, 330]
    }
  ]
};
```

### 饼图

```javascript
const pieOption = {
  title: { text: '销售占比', left: 'center' },
  tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', left: 'left', top: 'middle' },
  series: [{
    name: '销售占比', type: 'pie',
    radius: ['40%', '70%'], center: ['60%', '50%'],
    avoidLabelOverlap: true,
    itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
    label: { show: true, formatter: '{b}: {d}%' },
    data: [
      { value: 1048, name: '华东区' },
      { value: 735, name: '华北区' },
      { value: 580, name: '华南区' },
      { value: 484, name: '西北区' },
      { value: 300, name: '西南区' }
    ]
  }]
};
```

---

## 3. 响应式配置

```javascript
const responsiveOption = {
  baseOption: {
    title: { text: '销售数据' },
    legend: { data: ['销售额'] },
    xAxis: { type: 'category', data: [] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [] }]
  },
  media: [
    // 大屏 (≥1200px)
    {
      query: { minWidth: 1200 },
      option: {
        legend: { orient: 'horizontal', top: 10 },
        grid: { left: '10%', right: '10%' }
      }
    },
    // 中屏 (768-1199px)
    {
      query: { minWidth: 768, maxWidth: 1199 },
      option: {
        legend: { orient: 'horizontal', top: 10 },
        grid: { left: '15%', right: '10%' }
      }
    },
    // 小屏 (<768px)
    {
      query: { maxWidth: 767 },
      option: {
        legend: { orient: 'vertical', left: 10, top: 40 },
        grid: { left: '20%', right: '5%', top: 80 },
        xAxis: { axisLabel: { rotate: 45 } }
      }
    }
  ]
};
```

---

## 4. 主题定制

```javascript
// theme.js
const customTheme = {
  color: [
    '#5470c6', '#91cc75', '#fac858', '#ee6666',
    '#73c0de', '#3ba272', '#fc8452', '#9a60b4'
  ],
  backgroundColor: 'transparent',
  textStyle: {},
  title: {
    textStyle: { color: '#464646' },
    subtextStyle: { color: '#6E7079' }
  },
  line: {
    itemStyle: { borderWidth: 1 },
    lineStyle: { width: 2 },
    symbolSize: 4,
    symbol: 'emptyCircle',
    smooth: false
  },
  bar: {
    itemStyle: { barBorderWidth: 0, barBorderColor: '#ccc' }
  }
};

// 注册主题
echarts.registerTheme('custom', customTheme);

// 使用
echarts.init(dom, 'custom');
```

---

## 5. 按需加载

```javascript
// 按需引入减小包体积
import * as echarts from 'echarts/core';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  BarChart, LineChart, PieChart,
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  CanvasRenderer
]);

export default echarts;
```

---

## 6. 大数据优化配置

```javascript
// ❌ 错误：大数据无优化（卡顿）
const badOption = {
  series: [{
    type: 'line',
    data: largeDataArray  // 10000+ 数据点
  }]
};

// ✅ 正确：启用大数据优化
const goodOption = {
  series: [{
    type: 'line',
    data: largeDataArray,
    large: true,
    largeThreshold: 2000,
    sampling: 'lttb',  // Largest-Triangle-Three-Buckets
    animation: false,
    symbol: 'none',
    showSymbol: false
  }]
};
```
