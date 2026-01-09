---
name: echarts-patterns
description: |
  ECharts 数据可视化最佳实践。当涉及图表、数据可视化、统计图时自动触发。
  关键词：echarts、chart、图表、饼图、柱状图、折线图、可视化、统计。
  【数据可视化】包含图表配置、响应式、主题定制、性能优化。
version: 2.0.0
allowed-tools: Read, Grep, Glob
---

# ECharts 数据可视化最佳实践

## 项目架构

```
src/
├── components/
│   └── Charts/
│       ├── EChart.vue           # 通用 ECharts 封装
│       ├── LineChart.vue        # 折线图组件
│       ├── BarChart.vue         # 柱状图组件
│       └── PieChart.vue         # 饼图组件
├── config/
│   └── echarts/
│       ├── theme.ts             # 自定义主题
│       └── responsive.ts        # 响应式配置
└── utils/
    └── chartUtils.ts            # 图表工具函数

技术栈：
- ECharts 5.x
- Vue 2.x / Vue 3.x / React
```

---

## 1. 硬性约束 (Hard Constraints)

### 生命周期约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 销毁时必须 dispose | 防止内存泄漏 | `grep -rln "echarts.init" src/ --include="*.vue" \| xargs grep -L "dispose()"` | 🔴 Critical |
| resize 监听必须清理 | 防止事件堆积 | `grep -rln "addEventListener.*resize" src/ --include="*.vue" \| xargs grep -L "removeEventListener"` | 🔴 Critical |
| 必须在 nextTick 后初始化 | 容器尺寸确定 | `grep -A5 "mounted()" src/ --include="*.vue" \| grep "echarts.init" \| grep -v "nextTick"` | 🔴 Critical |

### 配置约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 大数据必须启用 large 模式 | >2000 数据点 | `grep -rn "type.*line\\|type.*bar" src/ --include="*.vue" \| xargs grep -L "large.*true"` | 🟡 Warning |
| 必须处理空数据 | 避免报错 | `grep -A20 "setOption" src/ --include="*.vue" \| grep -v "data.*length\\|!data\\|isEmpty"` | 🟡 Warning |
| 禁止频繁完整 setOption | 使用增量更新 | `grep -rn "setOption.*true" src/ --include="*.vue"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 容器尺寸为 0 时初始化

**问题**：容器未渲染完成就调用 `echarts.init()`，导致图表尺寸为 0。

**检测**：
```bash
# 检测 mounted 中直接调用 echarts.init
grep -A5 "mounted()" src/ -r --include="*.vue" | \
  grep "echarts.init" | grep -v "nextTick"

# 检测无 nextTick 的初始化
grep -B5 "echarts.init" src/ -r --include="*.vue" | \
  grep -v "$nextTick\|this.\$nextTick\|onMounted"
```

**修正**：
```javascript
// ❌ 错误：容器可能尺寸为 0
mounted() {
  this.chart = echarts.init(this.$refs.chartRef);  // 可能失败
  this.chart.setOption(this.option);
}

// ✅ 正确：确保容器渲染完成
mounted() {
  this.$nextTick(() => {
    this.initChart();
  });
}

// ✅ Vue 3 Composition API
onMounted(() => {
  nextTick(() => {
    chart.value = echarts.init(chartRef.value, theme);
    chart.value.setOption(option.value);
  });
});
```

---

### 反模式 2.2: 忘记销毁实例

**问题**：组件销毁时未调用 `dispose()`，导致内存泄漏和事件残留。

**检测**：
```bash
# 检测使用 echarts.init 但无 dispose
grep -rln "echarts.init" src/ --include="*.vue" | \
  xargs grep -L "dispose()"

# 检测 beforeDestroy 中是否有清理
grep -A10 "beforeDestroy\|beforeUnmount" src/ --include="*.vue" | \
  grep -v "dispose\|chart.*null"
```

**修正**：
```javascript
// ❌ 错误：未销毁实例
beforeDestroy() {
  // 什么都没做，内存泄漏！
}

// ✅ 正确：完整清理
beforeDestroy() {
  if (this.chart) {
    this.chart.dispose();
    this.chart = null;
  }
  if (this.resizeHandler) {
    window.removeEventListener('resize', this.resizeHandler);
  }
}

// ✅ Vue 3 Composition API
onBeforeUnmount(() => {
  chart.value?.dispose();
  chart.value = null;
  window.removeEventListener('resize', resizeHandler);
});
```

---

### 反模式 2.3: 频繁完整 setOption

**问题**：每次数据变化都完整设置 option，性能浪费。

**检测**：
```bash
# 检测 watch 中的完整 setOption
grep -A10 "watch:" src/ -r --include="*.vue" | \
  grep "setOption" | grep -v "merge.*false\|notMerge"

# 检测频繁 setOption 调用
grep -rn "setOption.*this.option\|setOption.*option" src/ --include="*.vue"
```

**修正**：
```javascript
// ❌ 错误：每次都完整设置
watch: {
  data() {
    this.chart.setOption(this.fullOption);  // 完整替换
  }
}

// ✅ 正确：增量更新
watch: {
  data(newData) {
    this.chart.setOption({
      series: [{ data: newData }]  // 只更新变化部分
    });
  }
}

// ✅ 正确：使用 appendData 追加
appendData(newData) {
  this.chart.appendData({
    seriesIndex: 0,
    data: newData
  });
}
```

---

### 反模式 2.4: resize 监听未防抖

**问题**：resize 事件触发频繁，导致图表频繁重绘。

**检测**：
```bash
# 检测 resize 监听是否有防抖
grep -A5 "addEventListener.*resize" src/ -r --include="*.vue" | \
  grep -v "debounce\|throttle\|setTimeout"

# 检测 resize 处理函数
grep -rn "window.onresize\|addEventListener.*resize" src/ --include="*.vue"
```

**修正**：
```javascript
// ❌ 错误：无防抖
mounted() {
  window.addEventListener('resize', () => {
    this.chart.resize();  // 每次都触发
  });
}

// ✅ 正确：使用防抖
import { debounce } from 'lodash';

mounted() {
  this.resizeHandler = debounce(() => {
    this.chart?.resize();
  }, 100);
  window.addEventListener('resize', this.resizeHandler);
}

beforeDestroy() {
  window.removeEventListener('resize', this.resizeHandler);
}
```

---

### 反模式 2.5: 大数据未启用优化

**问题**：大数据量时未启用 large 模式和采样，导致渲染卡顿。

**检测**：
```bash
# 检测大数据配置是否有优化
grep -A20 "series:" src/ -r --include="*.vue" | \
  grep "type.*line\|type.*bar" | \
  grep -v "large\|sampling\|largeThreshold"

# 统计 data 数组长度判断
grep -rn "data.*length.*>" src/ --include="*.vue" | head -5
```

**修正**：
```javascript
// ❌ 错误：大数据无优化（卡顿）
const option = {
  series: [{
    type: 'line',
    data: largeDataArray  // 10000+ 数据点
  }]
};

// ✅ 正确：启用大数据优化
const option = {
  series: [{
    type: 'line',
    data: largeDataArray,
    // 大数据优化
    large: true,
    largeThreshold: 2000,
    // 采样算法
    sampling: 'lttb',  // Largest-Triangle-Three-Buckets
    // 关闭动画
    animation: false,
    // 符号优化
    symbol: 'none',
    showSymbol: false
  }]
};
```

---


## 3. 最佳实践 (Golden Paths)

> 📖 **详见**: [CODE_EXAMPLES.md](./CODE_EXAMPLES.md) - 包含 Vue/React 封装、常用图表配置、响应式、主题定制、按需加载、大数据优化

| 类别 | 内容 |
|------|------|
| Vue 2 封装 | 基础组件、resize 监听、事件绑定 |
| 常用图表 | 折线图（双Y轴）、饼图（环形） |
| 响应式 | media query 配置、断点适配 |
| 主题定制 | 自定义主题注册和使用 |
| 按需加载 | 减小包体积的模块化引入 |
| 大数据优化 | sampling、large 模式、关闭动画 |


---

## 4. 自我验证 (Self-Verification)

### ECharts 合规审计脚本

```bash
#!/bin/bash
# echarts-audit.sh - ECharts 代码合规检查

echo "📊 ECharts 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测未销毁实例
echo -e "\n🧹 检测实例销毁..."
INIT_FILES=$(grep -rln "echarts.init" src/ --include="*.vue" 2>/dev/null)
MISSING_DISPOSE=""

for file in $INIT_FILES; do
    if ! grep -q "dispose()" "$file" 2>/dev/null; then
        MISSING_DISPOSE="$MISSING_DISPOSE\n  - $file"
    fi
done

if [ -n "$MISSING_DISPOSE" ]; then
    echo "❌ 以下文件缺少 dispose():$MISSING_DISPOSE"
    ((ERRORS++))
else
    echo "✅ 实例销毁正确"
fi

# 2. 检测 resize 监听清理
echo -e "\n🔄 检测 resize 监听..."
RESIZE_FILES=$(grep -rln "addEventListener.*resize" src/ --include="*.vue" 2>/dev/null)
MISSING_REMOVE=""

for file in $RESIZE_FILES; do
    if ! grep -q "removeEventListener.*resize" "$file" 2>/dev/null; then
        MISSING_REMOVE="$MISSING_REMOVE\n  - $file"
    fi
done

if [ -n "$MISSING_REMOVE" ]; then
    echo "❌ 以下文件 resize 监听未清理:$MISSING_REMOVE"
    ((ERRORS++))
else
    echo "✅ resize 监听正确清理"
fi

# 3. 检测 nextTick 初始化
echo -e "\n⏳ 检测初始化时机..."
NO_NEXTTICK=$(grep -B5 "echarts.init" src/ -r --include="*.vue" 2>/dev/null | \
  grep -v "nextTick\|onMounted" | grep -c "mounted()" || echo "0")

if [ "$NO_NEXTTICK" -gt 0 ]; then
    echo "⚠️ 可能有 $NO_NEXTTICK 处未在 nextTick 中初始化"
else
    echo "✅ 初始化时机正确"
fi

# 4. 检测防抖使用
echo -e "\n⚡ 检测 resize 防抖..."
RESIZE_NO_DEBOUNCE=$(grep -A5 "addEventListener.*resize" src/ -r --include="*.vue" 2>/dev/null | \
  grep -v "debounce\|throttle" | grep -c "resize" || echo "0")

if [ "$RESIZE_NO_DEBOUNCE" -gt 0 ]; then
    echo "⚠️ 可能有 resize 监听未使用防抖"
else
    echo "✅ resize 已使用防抖"
fi

# 5. 检测大数据优化
echo -e "\n📈 检测大数据优化..."
LARGE_DATA=$(grep -rn "series:" src/ --include="*.vue" 2>/dev/null | \
  grep -c "large.*true" || echo "0")

if [ "$LARGE_DATA" -eq 0 ]; then
    echo "💡 提示：如有大数据场景，建议启用 large 模式"
else
    echo "✅ 已发现 $LARGE_DATA 处大数据优化配置"
fi

# 6. 检测空数据处理
echo -e "\n📭 检测空数据处理..."
EMPTY_CHECK=$(grep -rn "setOption" src/ --include="*.vue" 2>/dev/null | wc -l | tr -d ' ')
EMPTY_GUARD=$(grep -rn "data.*length\|!data\|isEmpty" src/ --include="*.vue" 2>/dev/null | wc -l | tr -d ' ')

if [ "$EMPTY_GUARD" -eq 0 ] && [ "$EMPTY_CHECK" -gt 0 ]; then
    echo "⚠️ 建议添加空数据处理逻辑"
else
    echo "✅ 已有空数据处理逻辑"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ ECharts 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 使用 `nextTick` 确保容器渲染后再初始化
- [ ] `beforeDestroy` 中调用 `chart.dispose()`
- [ ] `resize` 监听使用 `debounce` 并在销毁时移除
- [ ] 数据变化时增量更新 `setOption`，不完整替换
- [ ] 大数据 (>2000点) 启用 `large: true` 和 `sampling`
- [ ] 处理空数据场景，避免报错
- [ ] 按需引入减小包体积

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `zustand-patterns` | 图表数据状态管理 |
| `react-query-patterns` | 图表数据获取和缓存 |
| `lowcode-engine-patterns` | 配置驱动图表生成 |
| `h5-responsive` | 移动端图表适配 |

### 关联文件

- `src/components/Charts/`
- `src/views/dashboard/`
- `src/config/echarts/theme.ts`

---

**✅ ECharts Patterns v2.0.0** | **标准 4 Section 已集成**
