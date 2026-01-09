---
name: apple-ui-scientist
description: "Apple UI 科学家。当用户需要：(1) 设计 iOS/H5 手势交互 (2) 添加触觉反馈 Haptic (3) 实现弹簧动画 (4) 应用 HIG 设计规范 (5) 创建毛玻璃/暗色模式效果时触发。用于打造极致的移动端用户体验。"
---

# Apple UI Scientist

## 核心原则

> **Clarity · Deference · Depth**

## 手势映射

| 手势 | H5 实现 | 用途 |
|------|--------|------|
| Tap | onClick | 选择 |
| Long Press | useLongPress(500ms) | 上下文菜单 |
| Swipe | drag="x" + onDragEnd | 导航/删除 |
| Pinch | touch events | 缩放 |

## 触觉反馈

```typescript
function triggerHaptic(type: "light" | "medium" | "heavy") {
  if ("vibrate" in navigator) {
    navigator.vibrate({ light: 10, medium: 20, heavy: 30 }[type]);
  }
}
```

## 动效参数

| 场景 | Duration | Type |
|------|----------|------|
| 微交互 | 0.1-0.2s | ease-out |
| 页面过渡 | 0.3-0.5s | spring |
| 按钮点击 | - | scale(0.95) + spring |

## 视觉规范

```css
/* 毛玻璃 */
.glass {
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(20px);
}

/* 阴影层级 */
--shadow-1: 0 1px 2px rgba(0,0,0,0.05);  /* 卡片 */
--shadow-2: 0 4px 12px rgba(0,0,0,0.1);  /* 弹出 */
--shadow-3: 0 12px 24px rgba(0,0,0,0.15); /* 模态 */
```

## 检查清单

- [ ] 点击区域 ≥ 44x44pt
- [ ] 对比度 ≥ 4.5:1
- [ ] 动效 ≤ 500ms
- [ ] 支持暗色模式
