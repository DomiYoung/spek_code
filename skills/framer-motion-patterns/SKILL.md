---
name: framer-motion-patterns
description: |
  Framer Motion 动画专家 - 过渡、手势、布局动画。
  Use when:
  - 实现动画、过渡效果
  - 手势交互、拖拽
  - 布局动画、列表动画
  触发词：动画、animate、transition、motion、gesture、framer-motion
  Related Skills: reactflow-patterns, shadcn-ui-patterns, tailwindcss-patterns
allowed-tools: Read, Grep, Glob
---

# Framer Motion 动画模式

## 基础动画

### 1. 入场/退场动画

```typescript
import { motion, AnimatePresence } from 'framer-motion';

// 淡入淡出
const fadeVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

function FadeComponent({ isVisible }: { isVisible: boolean }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          variants={fadeVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.3 }}
        >
          内容
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// 滑入动画
const slideVariants = {
  initial: { x: -100, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  exit: { x: 100, opacity: 0 },
};
```

### 2. 列表动画

```typescript
const listVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,  // 子元素依次出现
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

function AnimatedList({ items }: { items: Item[] }) {
  return (
    <motion.ul variants={listVariants} initial="hidden" animate="visible">
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### 3. 布局动画

```typescript
// 自动布局动画
function LayoutAnimation() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="grid">
      {items.map((item) => (
        <motion.div
          key={item.id}
          layoutId={item.id}  // 共享布局 ID
          onClick={() => setSelected(item.id)}
        >
          {item.content}
        </motion.div>
      ))}

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={selected}  // 相同 layoutId 自动过渡
            className="modal"
          >
            展开内容
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### 4. 手势交互

```typescript
function GestureCard() {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      drag="x"
      dragConstraints={{ left: -100, right: 100 }}
      dragElastic={0.2}
    >
      拖拽我
    </motion.div>
  );
}
```

## 性能优化

```typescript
// 使用 will-change
<motion.div style={{ willChange: 'transform' }} />

// 避免触发重排
// ✅ 好：transform, opacity
// ❌ 差：width, height, left, top

// 减少不必要的重渲染
const MotionComponent = memo(({ isOpen }: { isOpen: boolean }) => (
  <motion.div animate={{ opacity: isOpen ? 1 : 0 }} />
));
```

## 常见陷阱

### ❌ 陷阱 1：忘记 AnimatePresence

```typescript
// ❌ 错误：exit 动画不生效
{isVisible && <motion.div exit={{ opacity: 0 }} />}

// ✅ 正确：包裹 AnimatePresence
<AnimatePresence>
  {isVisible && <motion.div exit={{ opacity: 0 }} />}
</AnimatePresence>
```

### ❌ 陷阱 2：layoutId 冲突

```typescript
// ❌ 错误：相同 layoutId 导致异常
<motion.div layoutId="card" />
<motion.div layoutId="card" />  // 冲突！

// ✅ 正确：唯一 layoutId
<motion.div layoutId={`card-${id}`} />
```

---

**✅ Framer Motion Skill 已集成**
