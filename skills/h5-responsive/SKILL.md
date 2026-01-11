---
name: h5-responsive
description: |
  H5 移动端响应式专家 - 移动适配。
  Use when:
  - 移动端适配、响应式布局
  - rem、vw、媒体查询
  - 触摸优化
  触发词：响应式、mobile、移动端、rem、vw、@media、viewport
  Related Skills: tailwindcss-patterns, shadcn-ui-patterns, experts/frontend
allowed-tools: Read, Grep, Glob
---

# H5 移动端响应式开发

## Viewport 配置

### 基础配置

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

### 属性说明

| 属性 | 说明 | 推荐值 |
|------|------|--------|
| width | 视口宽度 | device-width |
| initial-scale | 初始缩放 | 1.0 |
| maximum-scale | 最大缩放 | 1.0 |
| minimum-scale | 最小缩放 | 1.0 |
| user-scalable | 允许缩放 | no |

## 响应式单位

### 单位对比

| 单位 | 说明 | 适用场景 |
|------|------|---------|
| px | 固定像素 | 边框、小图标 |
| rem | 相对根元素 | 字体、间距 |
| vw/vh | 视口百分比 | 全屏布局 |
| % | 相对父元素 | 弹性宽度 |
| em | 相对当前元素 | 特定场景 |

### rem 方案

```javascript
// 动态设置根字体大小
(function setRem() {
  const baseWidth = 375; // 设计稿宽度
  const baseFontSize = 16; // 基准字体

  function calc() {
    const clientWidth = document.documentElement.clientWidth;
    const scale = clientWidth / baseWidth;
    const fontSize = baseFontSize * Math.min(scale, 2);
    document.documentElement.style.fontSize = fontSize + 'px';
  }

  calc();
  window.addEventListener('resize', calc);
})();
```

```css
/* 使用 rem */
.container {
  padding: 1rem; /* 16px at 375px */
  font-size: 0.875rem; /* 14px */
}

/* PostCSS 自动转换 */
/* postcss-pxtorem 配置 */
```

### vw 方案（推荐）

```css
/* 直接使用 vw */
.container {
  padding: 4.267vw; /* 16/375*100 */
  font-size: 3.733vw; /* 14/375*100 */
}

/* 或使用 CSS 函数 */
:root {
  --vw: 1vw;
}

.container {
  /* 375 设计稿下 16px */
  padding: calc(16 * var(--vw) * 100 / 375);
}
```

### postcss-px-to-viewport 配置

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    'postcss-px-to-viewport': {
      viewportWidth: 375,
      viewportHeight: 667,
      unitPrecision: 5,
      viewportUnit: 'vw',
      selectorBlackList: [],
      minPixelValue: 1,
      mediaQuery: false
    }
  }
};
```

## 媒体查询

### 断点设计

```css
/* 移动优先 (Mobile First) */
.container {
  /* 默认移动端样式 */
  padding: 16px;
}

/* 平板 */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* 桌面 */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* 大屏 */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

### 常用断点

| 设备 | 断点 | 说明 |
|------|------|------|
| 手机 | < 768px | 默认样式 |
| 平板 | 768px - 1023px | @media (min-width: 768px) |
| 桌面 | 1024px - 1439px | @media (min-width: 1024px) |
| 大屏 | ≥ 1440px | @media (min-width: 1440px) |

### 横竖屏

```css
/* 竖屏 */
@media (orientation: portrait) {
  .container {
    flex-direction: column;
  }
}

/* 横屏 */
@media (orientation: landscape) {
  .container {
    flex-direction: row;
  }
}
```

## Flexbox 布局

### 常用模式

```css
/* 居中 */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 两端对齐 */
.between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 等分 */
.equal {
  display: flex;
}
.equal > * {
  flex: 1;
}

/* 固定 + 弹性 */
.fixed-flex {
  display: flex;
}
.fixed-flex .fixed {
  width: 100px;
  flex-shrink: 0;
}
.fixed-flex .flex {
  flex: 1;
  min-width: 0; /* 防止溢出 */
}
```

## Grid 布局

### 响应式网格

```css
.grid {
  display: grid;
  gap: 16px;

  /* 自适应列数 */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

/* 或使用媒体查询 */
.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr; /* 移动端单列 */
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr); /* 平板双列 */
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr); /* 桌面三列 */
  }
}
```

## 图片响应式

### srcset 和 sizes

```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="
    (max-width: 400px) 100vw,
    (max-width: 800px) 50vw,
    33vw
  "
  alt="响应式图片"
>
```

### picture 元素

```html
<picture>
  <source media="(min-width: 1024px)" srcset="desktop.jpg">
  <source media="(min-width: 768px)" srcset="tablet.jpg">
  <img src="mobile.jpg" alt="响应式图片">
</picture>
```

### CSS 背景图

```css
.hero {
  background-image: url('mobile.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('desktop.jpg');
  }
}

/* 或使用 image-set */
.hero {
  background-image: image-set(
    url('image-1x.jpg') 1x,
    url('image-2x.jpg') 2x
  );
}
```

## 触摸优化

### 触摸目标

```css
/* 最小触摸区域 44x44px */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  padding: 12px;
}

/* 增加点击区域 */
.btn {
  position: relative;
}
.btn::after {
  content: '';
  position: absolute;
  top: -10px;
  right: -10px;
  bottom: -10px;
  left: -10px;
}
```

### 禁用默认行为

```css
/* 禁用长按菜单 */
.no-select {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
}

/* 禁用点击高亮 */
.no-tap-highlight {
  -webkit-tap-highlight-color: transparent;
}

/* 流畅滚动 */
.scroll {
  -webkit-overflow-scrolling: touch;
  overflow-y: auto;
}
```

## 安全区域

### iPhone 刘海屏

```css
/* 使用 env() 函数 */
.container {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* 底部固定元素 */
.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
}
```

## 常见陷阱

### ❌ 陷阱 1：1px 边框问题

```css
/* ❌ 在高 DPI 屏幕上会变粗 */
.border {
  border: 1px solid #ddd;
}

/* ✅ 使用 transform 缩放 */
.border {
  position: relative;
}
.border::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 200%;
  height: 200%;
  border: 1px solid #ddd;
  transform: scale(0.5);
  transform-origin: left top;
  pointer-events: none;
}
```

### ❌ 陷阱 2：300ms 点击延迟

```css
/* 现代浏览器已修复，但仍需设置 */
html {
  touch-action: manipulation;
}
```

### ❌ 陷阱 3：滚动穿透

```javascript
// 打开弹窗时
document.body.style.overflow = 'hidden';
document.body.style.position = 'fixed';
document.body.style.width = '100%';
document.body.style.top = `-${window.scrollY}px`;

// 关闭弹窗时
const scrollY = document.body.style.top;
document.body.style.overflow = '';
document.body.style.position = '';
document.body.style.width = '';
document.body.style.top = '';
window.scrollTo(0, parseInt(scrollY || '0') * -1);
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `tailwindcss-patterns` | 原子化响应式 |
| `wechat-miniprogram` | 跨端适配 |

### 调试工具

- Chrome DevTools 设备模拟
- Xcode Simulator
- Android Studio Emulator
