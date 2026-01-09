# Core Web Vitals 深度指南

> **来源**: [Google Web Vitals](https://web.dev/vitals/) 官方标准
> **更新**: 2024 年标准（INP 替代 FID）

---

## 核心指标速查

### 2024 年 Core Web Vitals 三大指标

| 指标 | 全称 | 测量内容 | 优秀 | 需改进 | 差 |
|------|------|---------|------|--------|-----|
| **LCP** | Largest Contentful Paint | 最大内容绘制时间 | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** | Interaction to Next Paint | 交互到下一帧渲染 | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift | 累计布局偏移 | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

### 辅助指标

| 指标 | 全称 | 测量内容 | 优秀 | 需改进 | 差 |
|------|------|---------|------|--------|-----|
| **TTFB** | Time to First Byte | 首字节时间 | ≤ 800ms | 800ms - 1.8s | > 1.8s |
| **FCP** | First Contentful Paint | 首次内容绘制 | ≤ 1.8s | 1.8s - 3s | > 3s |
| **TBT** | Total Blocking Time | 总阻塞时间 | ≤ 200ms | 200ms - 600ms | > 600ms |

---

## LCP (Largest Contentful Paint)

### 定义

测量视口内最大内容元素（图片、视频、文本块）渲染完成的时间。

### 常见 LCP 元素

```
1. <img> 元素
2. <image> 内的 <svg> 元素
3. <video> 元素（使用 poster 图像）
4. 通过 url() 加载背景图的元素
5. 包含文本节点的块级元素
```

### 优化策略

#### 1. 优化资源加载

```html
<!-- ❌ 错误：无预加载 -->
<img src="hero.jpg" alt="Hero">

<!-- ✅ 正确：预加载 LCP 图片 -->
<link rel="preload" as="image" href="hero.jpg">
<img src="hero.jpg" alt="Hero">

<!-- ✅ 使用 fetchpriority 提升优先级 -->
<img src="hero.jpg" alt="Hero" fetchpriority="high">
```

#### 2. 优化服务端响应 (TTFB)

```typescript
// 服务端缓存配置
// ✅ 静态资源长期缓存
Cache-Control: public, max-age=31536000, immutable

// ✅ HTML 短期缓存 + 重验证
Cache-Control: public, max-age=0, must-revalidate
```

#### 3. 优化渲染阻塞资源

```html
<!-- ❌ 阻塞渲染的 CSS -->
<link rel="stylesheet" href="all-styles.css">

<!-- ✅ 关键 CSS 内联 + 非关键 CSS 异步 -->
<style>/* 关键 CSS 内联 */</style>
<link rel="preload" href="non-critical.css" as="style" onload="this.rel='stylesheet'">
```

#### 4. 图片优化

```html
<!-- ✅ 使用现代图片格式 -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero" width="1200" height="600">
</picture>

<!-- ✅ 响应式图片 -->
<img
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="hero-1200.jpg"
  alt="Hero"
>
```

### LCP 审计脚本

```typescript
// 使用 PerformanceObserver 检测 LCP
const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];

  console.log('LCP:', lastEntry.startTime);
  console.log('LCP Element:', lastEntry.element);

  // 判断是否达标
  if (lastEntry.startTime > 2500) {
    console.warn('❌ LCP 超过 2.5s，需要优化');
  } else {
    console.log('✅ LCP 达标');
  }
});

observer.observe({ type: 'largest-contentful-paint', buffered: true });
```

---

## INP (Interaction to Next Paint)

### 定义

测量用户交互（点击、触摸、键盘）到页面视觉响应的延迟。取页面生命周期内最差的交互延迟（排除异常值）。

### INP vs FID

| 对比 | FID（已废弃） | INP（2024+） |
|------|-------------|-------------|
| 测量内容 | 首次交互延迟 | 所有交互中最差的延迟 |
| 覆盖范围 | 仅首次 | 整个页面生命周期 |
| 更准确 | ❌ | ✅ |

### 优化策略

#### 1. 分解长任务

```typescript
// ❌ 长任务阻塞主线程
function processData(items: Item[]) {
  items.forEach(item => heavyComputation(item)); // 可能 > 50ms
}

// ✅ 使用 scheduler.yield() 让出主线程（Chrome 129+）
async function processData(items: Item[]) {
  for (const item of items) {
    heavyComputation(item);

    // 每处理一批后让出主线程
    if (scheduler.yield) {
      await scheduler.yield();
    }
  }
}

// ✅ 降级方案：使用 setTimeout
async function processDataFallback(items: Item[]) {
  const CHUNK_SIZE = 50;

  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => heavyComputation(item));

    // 让出主线程
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

#### 2. 优化事件处理器

```typescript
// ❌ 事件处理器执行重计算
onClick={() => {
  const result = expensiveCalculation(); // 阻塞
  setResult(result);
}}

// ✅ 使用 startTransition 标记为非紧急
import { startTransition } from 'react';

onClick={() => {
  // 立即响应 UI
  setIsLoading(true);

  // 非紧急更新
  startTransition(() => {
    const result = expensiveCalculation();
    setResult(result);
    setIsLoading(false);
  });
}}

// ✅ 使用 requestIdleCallback 延迟非关键任务
onClick={() => {
  // 立即响应
  updateUI();

  // 空闲时执行
  requestIdleCallback(() => {
    analytics.track('click');
    prefetchNextPage();
  });
}}
```

#### 3. 减少主线程工作

```typescript
// ❌ 同步 JSON 解析大数据
const data = JSON.parse(hugeJsonString);

// ✅ 使用 Web Worker 异步解析
const worker = new Worker('json-parser.worker.js');
worker.postMessage(hugeJsonString);
worker.onmessage = (e) => {
  const data = e.data;
  updateUI(data);
};
```

### INP 审计脚本

```typescript
// 使用 PerformanceObserver 检测 INP
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    // entry.duration = 交互延迟
    console.log(`Interaction: ${entry.name}, Duration: ${entry.duration}ms`);

    if (entry.duration > 200) {
      console.warn('⚠️ 交互延迟 > 200ms');
      console.log('Target:', entry.target);
    }
  }
});

observer.observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

---

## CLS (Cumulative Layout Shift)

### 定义

测量页面生命周期内所有意外布局偏移的累计分数。

### CLS 计算公式

```
CLS = impact fraction × distance fraction

impact fraction = 受影响区域占视口比例
distance fraction = 元素移动距离占视口比例
```

### 常见 CLS 原因

| 原因 | 影响 | 解决方案 |
|------|------|---------|
| 无尺寸的图片/视频 | 加载后撑开空间 | 设置 width/height |
| 动态注入内容 | 推挤现有内容 | 预留空间 |
| Web 字体闪烁 (FOIT/FOUT) | 字体切换导致重排 | font-display: swap |
| 动态广告/嵌入 | 尺寸未知 | 容器预留空间 |

### 优化策略

#### 1. 为媒体预留空间

```html
<!-- ❌ 无尺寸 - 导致 CLS -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ 设置尺寸 - 浏览器预留空间 -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ 使用 aspect-ratio CSS -->
<style>
.responsive-img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}
</style>
<img class="responsive-img" src="photo.jpg" alt="Photo">
```

#### 2. 优化字体加载

```css
/* ❌ 字体闪烁 */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
}

/* ✅ 使用 font-display: swap */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
}

/* ✅ 使用 size-adjust 匹配后备字体度量 */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
}
```

```html
<!-- ✅ 预加载关键字体 -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

#### 3. 动态内容预留空间

```typescript
// ❌ 动态内容推挤页面
{showBanner && <Banner />}

// ✅ 使用 min-height 预留空间
<div style={{ minHeight: showBanner ? 'auto' : '80px' }}>
  {showBanner && <Banner />}
</div>

// ✅ 使用 CSS contain 限制布局影响
.dynamic-section {
  contain: layout;
}
```

#### 4. 动画使用 transform

```css
/* ❌ 触发布局的动画 */
.animate {
  animation: slide 0.3s;
}
@keyframes slide {
  from { top: 0; }
  to { top: 100px; }
}

/* ✅ 使用 transform（不触发布局） */
.animate {
  animation: slide 0.3s;
}
@keyframes slide {
  from { transform: translateY(0); }
  to { transform: translateY(100px); }
}
```

### CLS 审计脚本

```typescript
// 使用 PerformanceObserver 检测 CLS
let clsValue = 0;
let clsEntries: PerformanceEntry[] = [];

const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries() as any[]) {
    // 忽略用户输入后 500ms 内的偏移
    if (!entry.hadRecentInput) {
      clsValue += entry.value;
      clsEntries.push(entry);
    }
  }

  console.log('Current CLS:', clsValue.toFixed(4));

  if (clsValue > 0.1) {
    console.warn('❌ CLS 超过 0.1');
    console.log('导致偏移的元素:', clsEntries.map(e => (e as any).sources));
  }
});

observer.observe({ type: 'layout-shift', buffered: true });
```

---

## 测量工具

### 实验室工具（Lab）

| 工具 | 用途 | 特点 |
|------|------|------|
| **Lighthouse** | 整体审计 | Chrome DevTools 内置 |
| **WebPageTest** | 详细瀑布图 | 多地点测试 |
| **Chrome DevTools** | 实时调试 | Performance 面板 |

### 真实用户数据（Field）

| 工具 | 数据来源 | 特点 |
|------|---------|------|
| **CrUX** | Chrome 用户 | Google 官方数据 |
| **web-vitals.js** | 自行收集 | 可接入自有系统 |
| **PageSpeed Insights** | CrUX + Lighthouse | 综合报告 |

### web-vitals.js 集成

```typescript
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

// 上报到分析系统
function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    id: metric.id,
  });

  // 使用 sendBeacon 确保数据发送
  navigator.sendBeacon('/analytics', body);
}

// 监听所有 Core Web Vitals
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

---

## 审计清单

### LCP 检查清单

- [ ] LCP 元素是否预加载？（`<link rel="preload">`）
- [ ] 是否使用 `fetchpriority="high"`？
- [ ] 服务器 TTFB < 800ms？
- [ ] 是否有渲染阻塞资源？
- [ ] 图片是否使用现代格式（WebP/AVIF）？

### INP 检查清单

- [ ] 是否有长任务 > 50ms？
- [ ] 事件处理器是否使用 `startTransition`？
- [ ] 重计算是否移到 Web Worker？
- [ ] 是否使用 `requestIdleCallback` 延迟非关键任务？

### CLS 检查清单

- [ ] 所有图片/视频是否设置尺寸？
- [ ] 字体是否使用 `font-display: swap`？
- [ ] 动态内容是否预留空间？
- [ ] 动画是否使用 `transform` 而非布局属性？

---

## 禁止行为

| 行为 | 状态 | 正确做法 |
|------|------|---------|
| 不测量直接优化 | ❌ **Forbidden** | 先用 Lighthouse 测量基准 |
| 主观判断"够快了" | ❌ **Forbidden** | 用 Core Web Vitals 量化 |
| 忽略真实用户数据 | ❌ **Forbidden** | 结合 CrUX/web-vitals.js |
| 只看实验室数据 | ⚠️ **Warning** | Field 数据更能反映真实情况 |

---

## 参考资源

- [Google Web Vitals](https://web.dev/vitals/)
- [web-vitals.js](https://github.com/GoogleChrome/web-vitals)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [PageSpeed Insights](https://pagespeed.web.dev/)

**记住**: 优化目标是 **75th 百分位用户体验**，不是平均值。

