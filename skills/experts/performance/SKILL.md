---
name: performance-expert
type: Expert
version: 1.0.0
description: |
  性能优化专家 - 基于数据驱动的代码优化与性能工程。
  ① 帮我干什么：算法优化流程、包管理决策、Core Web Vitals 性能度量
  ② 什么时候出场：涉及性能、优化、卡顿、慢、内存、加载、包大小时自动调用
  ③ 和项目有无关系：适用于所有前端项目，是全局通用的性能优化专家
  关键词：性能、优化、卡顿、慢、内存、加载、LCP、FID、CLS、INP、TTFB、bundle、包大小
allowed-tools: "*"
---

# Performance Expert（性能优化专家）

> **核心理念**：数据驱动，不凭感觉。测量 → 分析 → 优化 → 验证。
> **禁止行为**：❌ "我觉得可以" ❌ "应该没问题" ❌ 跳过验证直接上线

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **禁止全量引入** | 禁止 `import _ from 'lodash'` 等全量导入 | `grep -E "import \* as|import _ from|from 'lodash'$" src/` |
| **禁止无尺寸媒体** | 图片/视频必须设置 width/height | `grep -rL "width=\|height=" --include="*.tsx" \| xargs grep -l "<img\|<video"` |
| **禁止长任务** | 单个同步任务 ≤ 50ms | Chrome DevTools Performance → Main Thread 长任务检测 |
| **禁止主观判断** | 必须有量化指标支撑 | 代码 Review 检查是否有 Lighthouse/DevTools 数据 |
| **Core Web Vitals** | LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 | `web-vitals` 库监控 + Lighthouse CI |
| **Bundle 大小** | 首屏 gzip ≤ 200KB | `webpack-bundle-analyzer` 或 `source-map-explorer` |
| **禁止 moment.js** | 使用 dayjs 或 date-fns | `grep -r "from 'moment'" src/` |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 不测量直接优化

**问题**: 凭感觉优化，可能优化非瓶颈或过度优化
**检测**: 优化 PR 无 Lighthouse 基准数据对比
**修正**:
```bash
# 必须先采集基准
lighthouse https://localhost:3000 --output=json --output-path=./baseline.json
# 优化后对比
lighthouse https://localhost:3000 --output=json --output-path=./optimized.json
```

### ❌ 内联对象/函数作为 Props

**问题**: 每次渲染创建新引用，导致子组件重渲染
**检测**: `grep -rE "style=\{\{|onClick=\{\\(\\)" src/`
**修正**:
```typescript
// ❌ 错误
<Component style={{ color: 'red' }} onClick={() => handleClick(id)} />

// ✅ 正确
const style = useMemo(() => ({ color: 'red' }), []);
const handleClickMemo = useCallback(() => handleClick(id), [id]);
<Component style={style} onClick={handleClickMemo} />
```

### ❌ 同步处理大数据

**问题**: 阻塞主线程，导致 INP 超标
**检测**: `grep -rE "\.forEach\(|\.map\(" src/ | grep -v "async\|await\|Promise"`
**修正**:
```typescript
// ❌ 阻塞主线程
items.forEach(item => heavyComputation(item));

// ✅ 分批处理
async function processInChunks(items, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(item => heavyComputation(item));
    await new Promise(resolve => setTimeout(resolve, 0)); // 让出主线程
  }
}
```

### ❌ 未预留媒体空间

**问题**: 图片加载后撑开布局，导致 CLS 超标
**检测**: `grep -rE "<img[^>]*>" src/ | grep -v "width=\|height=\|aspect-ratio"`
**修正**:
```html
<!-- ❌ 无尺寸 -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ 设置尺寸 -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ 或使用 aspect-ratio -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 16/9; width: 100%;">
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准化解决方案

### 3.1 按需引入模板

```typescript
// lodash - 必须使用 lodash-es 按需引入
import debounce from 'lodash-es/debounce';
import throttle from 'lodash-es/throttle';

// date-fns - 按需引入
import { format, parseISO } from 'date-fns';

// antd - 已支持 Tree Shaking，但仍建议具名导入
import { Button, Modal, Table } from 'antd';
```

### 3.2 虚拟滚动模板

```typescript
import { Virtuoso } from 'react-virtuoso';

// 大列表必须使用虚拟滚动 (>100 项)
<Virtuoso
  data={items}
  itemContent={(index, item) => <ListItem key={item.id} item={item} />}
  overscan={5}
/>
```

### 3.3 图片优化模板

```html
<!-- LCP 图片预加载 -->
<link rel="preload" as="image" href="hero.jpg">

<!-- 使用现代格式 + 响应式 -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img
    src="hero.jpg"
    alt="Hero"
    width="1200"
    height="600"
    fetchpriority="high"
    loading="eager"
  >
</picture>

<!-- 非首屏图片懒加载 -->
<img src="photo.jpg" alt="Photo" loading="lazy" width="400" height="300">
```

### 3.4 事件优化模板

```typescript
import { startTransition, useCallback } from 'react';

// 使用 startTransition 标记非紧急更新
const handleSearch = useCallback((query: string) => {
  setInputValue(query); // 紧急：立即响应输入

  startTransition(() => {
    setSearchResults(filterResults(query)); // 非紧急：可延迟
  });
}, []);

// 使用 requestIdleCallback 延迟非关键任务
const handleClick = useCallback(() => {
  updateUI(); // 立即响应

  requestIdleCallback(() => {
    analytics.track('click'); // 空闲时执行
    prefetchNextPage();
  });
}, []);
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前必须逐项检查

### 提交前检查清单

```markdown
## Performance Self-Audit ✓

### Core Web Vitals
- [ ] LCP ≤ 2.5s（Lighthouse 验证）
- [ ] INP ≤ 200ms（Performance 面板验证）
- [ ] CLS ≤ 0.1（Layout Shift 检测）

### Bundle 优化
- [ ] 无全量 lodash/moment 引入
- [ ] 新增包已检查 bundlephobia 大小
- [ ] 首屏 bundle ≤ 200KB gzip

### 渲染优化
- [ ] 大列表（>100项）使用虚拟滚动
- [ ] 无内联对象/函数作为 Props
- [ ] 昂贵计算使用 useMemo/useCallback

### 媒体优化
- [ ] 所有 img/video 设置 width/height
- [ ] LCP 图片使用 preload + fetchpriority
- [ ] 非首屏图片使用 loading="lazy"

### 验证完成
- [ ] Lighthouse Performance ≥ 90
- [ ] 优化前后对比数据已记录
```

### 自动审计脚本

```bash
#!/bin/bash
# performance-audit.sh - 放入 pre-commit hook

echo "🔍 Performance Audit..."

# 检查全量 lodash
if grep -rE "from 'lodash'$" src/; then
  echo "❌ 发现全量 lodash 引入，请使用 lodash-es 按需引入"
  exit 1
fi

# 检查 moment.js
if grep -r "from 'moment'" src/; then
  echo "❌ 禁止使用 moment.js，请使用 dayjs 或 date-fns"
  exit 1
fi

# 检查无尺寸图片
if grep -rE "<img[^>]*>" src/ | grep -v "width=\|height="; then
  echo "⚠️ 发现无尺寸图片，可能导致 CLS 问题"
fi

echo "✅ Performance Audit 通过"
```

---

## 🔴 强制执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    性能优化标准流程                               │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: 基准测量                                                │
│  ├── 使用 Chrome DevTools / Lighthouse 采集当前指标              │
│  ├── 记录 Core Web Vitals (LCP, FID/INP, CLS, TTFB)            │
│  └── 保存基准数据到 Memory                                       │
├─────────────────────────────────────────────────────────────────┤
│  Step 2: 问题定位                                                │
│  ├── Performance 面板火焰图分析                                  │
│  ├── Network 瀑布图分析                                          │
│  └── 识别瓶颈：渲染/脚本/网络/内存                               │
├─────────────────────────────────────────────────────────────────┤
│  Step 3: 方案设计                                                │
│  ├── 选择合适的优化算法（见 references/optimization-algorithms.md）│
│  ├── 评估包引入必要性（见 references/package-management.md）      │
│  └── 输出优化方案文档                                            │
├─────────────────────────────────────────────────────────────────┤
│  Step 4: 实施优化                                                │
│  ├── 按方案逐项实施                                              │
│  ├── 每项优化后立即测量                                          │
│  └── 记录优化效果                                                │
├─────────────────────────────────────────────────────────────────┤
│  Step 5: 验证报告                                                │
│  ├── 对比优化前后 Core Web Vitals                                │
│  ├── 生成性能优化报告                                            │
│  └── 达标才算完成（见下方标准）                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Core Web Vitals 达标标准

> **来源**: [Google Web Vitals](https://web.dev/vitals/)

| 指标 | 全称 | 优秀 (绿) | 需改进 (黄) | 差 (红) |
|------|------|----------|------------|--------|
| **LCP** | Largest Contentful Paint | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** | Interaction to Next Paint | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| **TTFB** | Time to First Byte | ≤ 800ms | 800ms - 1.8s | > 1.8s |
| **FCP** | First Contentful Paint | ≤ 1.8s | 1.8s - 3s | > 3s |

### 项目达标要求

```
┌─ 性能达标标准 ───────────────────────────────┐
│ □ LCP ≤ 2.5s        (首屏核心内容加载)       │
│ □ INP ≤ 200ms       (交互响应延迟)           │
│ □ CLS ≤ 0.1         (布局稳定性)             │
│ □ TTFB ≤ 800ms      (服务器响应时间)         │
│ □ Bundle Size 首屏 ≤ 200KB (gzip)           │
│ □ 长任务 ≤ 50ms     (无阻塞主线程)           │
└──────────────────────────────────────────────┘
```

---

## 🧮 算法优化决策框架

### 复杂度优先级

```
O(1) > O(log n) > O(n) > O(n log n) > O(n²) > O(2^n)
```

### 常见优化模式速查

| 场景 | 原始复杂度 | 优化算法 | 优化后 |
|------|-----------|---------|--------|
| 列表搜索 | O(n) | Hash Map / Set | O(1) |
| 重复计算 | O(n×m) | Memoization | O(n+m) |
| 深层遍历 | O(n²) | 扁平化 + 索引 | O(n) |
| 频繁 DOM | O(n) | 批量更新 / RAF | O(1) |
| 大列表渲染 | O(n) | 虚拟滚动 | O(k) 可视区 |

**详细算法库**: 见 `references/optimization-algorithms.md`

---

## 📦 包管理决策框架

### 引入新包前必答 5 问

```
┌─ 包引入决策清单 ─────────────────────────────┐
│ 1. 真的需要吗？                              │
│    □ 能否用原生 API 实现？                   │
│    □ 项目已有类似功能吗？                    │
│                                              │
│ 2. 包质量如何？                              │
│    □ npm 周下载量 > 10k？                    │
│    □ 最近 6 个月有更新？                     │
│    □ GitHub Stars > 1k？                     │
│    □ 无已知安全漏洞？                        │
│                                              │
│ 3. 大小影响多少？                            │
│    □ bundlephobia.com 检查大小               │
│    □ 支持 Tree Shaking？                     │
│    □ 对首屏 Bundle 影响 < 20KB？             │
│                                              │
│ 4. 框架兼容吗？                              │
│    □ 支持当前 React/Vue 版本？               │
│    □ 支持 TypeScript？                       │
│    □ 支持 ESM？                              │
│                                              │
│ 5. 引入方式？                                │
│    □ 按需引入（推荐）                        │
│    □ 动态 import（次选）                     │
│    □ 全量引入（最后手段）                    │
└──────────────────────────────────────────────┘
```

### 按需引入 vs 全量引入

```typescript
// ❌ 全量引入 - 打包整个 lodash (~70KB)
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ 按需引入 - 只打包 debounce (~1KB)
import debounce from 'lodash-es/debounce';
debounce(fn, 300);

// ✅ 动态引入 - 首屏不加载
const { debounce } = await import('lodash-es');
```

**详细包管理策略**: 见 `references/package-management.md`

---

## 🔬 性能测量工具链

### Chrome DevTools 使用流程

```bash
# 1. Performance 面板
F12 → Performance → Record → 执行操作 → Stop
分析：
- Main Thread: 查看长任务 (红色标记 > 50ms)
- Network: 查看请求瀑布
- Frames: 查看帧率 (目标 60fps)

# 2. Lighthouse 审计
F12 → Lighthouse → Analyze page load
关注：
- Performance 分数 (目标 ≥ 90)
- Core Web Vitals 各项指标
- Opportunities 优化建议

# 3. Network 面板
F12 → Network → Disable cache → 刷新
分析：
- Waterfall: 请求时序
- Size: 资源大小
- Time: 加载时间
```

### 性能 API 埋点

```typescript
// 使用 Performance API 精确测量
const measureRender = (name: string) => {
  performance.mark(`${name}-start`);
  return () => {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);
    const measure = performance.getEntriesByName(name)[0];
    console.log(`${name}: ${measure.duration.toFixed(2)}ms`);
  };
};

// 使用
const endMeasure = measureRender('ComponentRender');
// ... 渲染逻辑
endMeasure();
```

---

## ⚡ 快速优化检查清单

### 渲染性能

- [ ] 使用 `React.memo` 避免不必要重渲染
- [ ] 使用 `useMemo` 缓存昂贵计算
- [ ] 使用 `useCallback` 稳定回调引用
- [ ] 长列表使用虚拟滚动 (react-virtuoso)
- [ ] 避免内联对象/函数作为 props

### 加载性能

- [ ] 路由级别代码分割 (`React.lazy`)
- [ ] 组件级别动态导入 (`import()`)
- [ ] 图片懒加载 (`loading="lazy"`)
- [ ] 预加载关键资源 (`<link rel="preload">`)
- [ ] 压缩资源 (gzip/brotli)

### 网络性能

- [ ] API 请求合并 (批量接口)
- [ ] 使用缓存策略 (staleTime/cacheTime)
- [ ] 避免重复请求 (React Query)
- [ ] 使用 CDN 加速静态资源
- [ ] 启用 HTTP/2

### 运行时性能

- [ ] 避免同步长任务 (> 50ms)
- [ ] 使用 Web Worker 处理重计算
- [ ] 防抖/节流高频事件
- [ ] 使用 requestAnimationFrame 动画
- [ ] 避免强制同步布局

---

## 📋 优化报告模板

```markdown
## 性能优化报告

**日期**: YYYY-MM-DD
**优化范围**: [页面/组件/模块名称]

### 优化前基准

| 指标 | 数值 | 评级 |
|------|------|------|
| LCP | X.Xs | 🟡/🔴 |
| INP | Xms | 🟡/🔴 |
| CLS | X.XX | 🟡/🔴 |
| Bundle Size | XXkB | - |

### 优化措施

1. [优化措施 1] - 预期效果
2. [优化措施 2] - 预期效果
3. ...

### 优化后数据

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| LCP | X.Xs | X.Xs | -XX% |
| INP | Xms | Xms | -XX% |
| CLS | X.XX | X.XX | -XX% |
| Bundle Size | XXkB | XXkB | -XX% |

### 结论

- [ ] 达标 (所有核心指标绿色)
- [ ] 部分达标 (需后续优化)
- [ ] 未达标 (需重新分析)
```

---

## 📚 参考资料

### Reference Files

详细指南请查阅：
- **`references/optimization-algorithms.md`** - 算法优化模式库
- **`references/package-management.md`** - 包管理决策详细指南
- **`references/web-vitals-guide.md`** - Core Web Vitals 深度指南

### 外部资源

- [Google Web Vitals](https://web.dev/vitals/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Bundlephobia](https://bundlephobia.com/) - 检查包大小
- [React Profiler](https://react.dev/reference/react/Profiler)

---

## ❌ 禁止行为

| 行为 | 状态 | 正确做法 |
|------|------|---------|
| 不测量直接优化 | ❌ **Forbidden** | 先用 Lighthouse 采集基准 |
| 主观判断"够快了" | ❌ **Forbidden** | 用 Core Web Vitals 量化 |
| 全量引入大型库 | ❌ **Forbidden** | 按需引入或动态导入 |
| 跳过优化验证 | ❌ **Forbidden** | 必须对比优化前后数据 |
| 过度优化 | ⚠️ **Warning** | 只优化真实瓶颈 |

---

**✅ 性能优化专家已就绪** | **数据驱动，不凭感觉**
