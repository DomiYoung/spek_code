---
name: tailwindcss-expert
description: "TailwindCSS 专家。当用户需要：(1) 配置设计系统 (2) 实现响应式布局 (3) 创建暗色模式 (4) 使用动画/过渡 (5) 抽象组件样式时触发。"
---

# TailwindCSS Expert

## 响应式断点

```html
<!-- Mobile First: sm(640) md(768) lg(1024) xl(1280) -->
<div class="text-sm md:text-base lg:text-lg">响应式</div>
```

## 常用组合

### 卡片
```html
<div class="bg-white rounded-xl shadow-lg p-6 border border-zinc-100">
```

### 渐变边框
```html
<div class="p-[1px] bg-gradient-to-br from-amber-400 to-amber-600 rounded-2xl">
  <div class="bg-white rounded-[15px] p-6">Content</div>
</div>
```

### 毛玻璃
```html
<div class="bg-white/80 backdrop-blur-md">Glassmorphism</div>
```

## 状态变体

```html
<button class="
  bg-blue-500 hover:bg-blue-600 
  active:scale-95 disabled:opacity-50
  transition-all duration-300
">
```

## 暗色模式

```html
<div class="bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white">
```

## 组件抽象

```tsx
// ✅ 推荐: 组件封装
function Button({ variant = "primary", children }) {
  const styles = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-zinc-100 text-zinc-900"
  };
  return <button className={`px-4 py-2 rounded-lg ${styles[variant]}`}>{children}</button>;
}
```

## 避免 ❌

- 过长类名列表 → 抽取组件
- 重复样式 → 使用 @apply (谨慎)
