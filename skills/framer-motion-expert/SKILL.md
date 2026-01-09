---
name: framer-motion-expert
description: "Framer Motion 专家。当用户需要：(1) 实现 React 动画 (2) 添加手势交互 drag/tap (3) 使用 Variants 编排 (4) 创建页面过渡 (5) 实现布局动画时触发。"
---

# Framer Motion Expert

## 基础动画

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.5 }}
/>
```

## 手势交互

```tsx
// Hover & Tap
<motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} />

// Drag
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  onDragEnd={(e, { offset }) => offset.x > 50 && handleSwipe()}
/>
```

## Variants 编排

```tsx
const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};
const item = { hidden: { y: 20 }, show: { y: 0 } };

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => <motion.li key={i} variants={item} />)}
</motion.ul>
```

## AnimatePresence

```tsx
<AnimatePresence>
  {isOpen && <motion.div exit={{ opacity: 0 }}>Modal</motion.div>}
</AnimatePresence>
```

## Layout 动画

```tsx
<motion.div layout />              // 自动动画位置变化
<motion.div layoutId="shared" />   // 跨组件共享动画
```

## 脉冲发光

```tsx
<motion.div
  animate={{ opacity: [0.1, 0.3, 0.1] }}
  transition={{ duration: 3, repeat: Infinity }}
  className="blur-2xl"
/>
```
