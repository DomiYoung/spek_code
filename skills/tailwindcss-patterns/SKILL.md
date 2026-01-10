---
name: tailwindcss-patterns
description: |
  TailwindCSS 原子化 CSS 最佳实践。当涉及 utility-first CSS、响应式设计、组件样式时自动触发。
  关键词：tailwind、tw、utility、原子化、className、responsive、dark mode、JIT。
  【原子化CSS】包含响应式设计、暗色模式、组件抽象、性能优化。
allowed-tools: Read, Grep, Glob
---

# TailwindCSS 原子化 CSS

## 核心理念

Tailwind 采用 Utility-First 哲学：用原子类组合实现样式，而非预设组件类。

---

## 1. 硬性约束 (Hard Constraints)

### 类名约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 禁止动态类名拼接 | 无法被 purge | `grep -rn "className={\`.*\${" src/ --include="*.tsx"` | 🔴 Critical |
| 必须使用 tailwind-merge 处理冲突 | 避免类名覆盖不确定 | `grep -rln "twMerge\|tailwind-merge" src/ --include="*.tsx"` | 🟡 Warning |
| 响应式必须 mobile-first | 从小到大排序 | 手动检查断点顺序 | 🟡 Warning |
| content 配置必须完整 | 否则样式被 purge | `grep -A5 "content:" tailwind.config.*` | 🔴 Critical |

### 配置约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 必须配置暗色模式策略 | class 或 media | `grep "darkMode" tailwind.config.*` | 🟡 Warning |
| 自定义颜色必须完整色阶 | 50-900 全覆盖 | `grep -A10 "colors:" tailwind.config.*` | 🟡 Warning |
| 禁止过度 @apply | 仅高频组件使用 | `grep -c "@apply" src/**/*.css` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 动态类名拼接

**问题**：使用模板字符串拼接类名，JIT 无法分析，导致样式被 purge 掉。

**检测**：
```bash
# 检测动态类名拼接
grep -rn "className={\`.*\${" src/ --include="*.tsx"

# 检测字符串拼接
grep -rn "className=.*+" src/ --include="*.tsx" | grep -v "cn(\|clsx(\|twMerge("
```

**修正**：
```tsx
// ❌ 错误：动态拼接（被 purge）
<div className={`text-${color}-500`} />  // JIT 无法分析

// ✅ 正确：使用映射对象
const colorMap = {
  primary: 'text-blue-500',
  secondary: 'text-gray-500',
  danger: 'text-red-500',
};
<div className={colorMap[color]} />

// ✅ 正确：使用 cva
const text = cva('', {
  variants: {
    color: {
      primary: 'text-blue-500',
      secondary: 'text-gray-500',
    }
  }
});
<div className={text({ color })} />
```

---

### 反模式 2.2: 类名冲突未合并

**问题**：同类型的 Tailwind 类叠加，覆盖结果不确定。

**检测**：
```bash
# 检测重复类型的类名
grep -rn "className=" src/ --include="*.tsx" | \
  grep "p-[0-9].*p-[0-9]\|m-[0-9].*m-[0-9]\|text-.*text-"

# 检测条件类名未使用合并工具
grep -rn "className={" src/ --include="*.tsx" | \
  grep "&&\|?" | grep -v "cn(\|clsx(\|twMerge("
```

**修正**：
```tsx
// ❌ 错误：类名冲突结果不确定
<div className="p-4 p-8" />  // 哪个生效？取决于 CSS 顺序

// ❌ 错误：条件类名未合并
<div className={`p-4 ${isLarge && 'p-8'}`} />

// ✅ 正确：使用 tailwind-merge
import { twMerge } from 'tailwind-merge';
<div className={twMerge('p-4', isLarge && 'p-8')} />

// ✅ 正确：使用 cn 工具函数
import { cn } from '@/lib/utils';
<div className={cn('p-4', isLarge && 'p-8')} />
```

---

### 反模式 2.3: 响应式断点顺序错误

**问题**：违反 mobile-first 原则，断点逻辑混乱。

**检测**：
```bash
# 检测响应式类名顺序
grep -rn "className=" src/ --include="*.tsx" | \
  grep "lg:.*md:\|xl:.*lg:\|2xl:.*xl:"
```

**修正**：
```tsx
// ❌ 错误：从大到小（逻辑混乱）
<div className="lg:hidden md:block sm:flex" />

// ✅ 正确：Mobile-first（从小到大）
<div className="flex sm:block md:hidden" />
// 解读：默认 flex，sm+ 变 block，md+ 隐藏
```

---

### 反模式 2.4: 过度使用 @apply

**问题**：每个样式都抽象成类，失去 Utility-First 的优势。

**检测**：
```bash
# 统计 @apply 使用次数
grep -c "@apply" src/**/*.css 2>/dev/null || echo "0"

# 检测简单样式也用 @apply
grep -B1 "@apply" src/**/*.css | grep -E "^\.[a-z-]+\s*\{"
```

**修正**：
```css
/* ❌ 错误：过度抽象 */
.text-blue { @apply text-blue-500; }
.margin-4 { @apply m-4; }

/* ✅ 正确：只抽象高频复杂组件 */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded-lg
           hover:bg-blue-600 focus:ring-2 focus:ring-blue-300
           transition-colors duration-200;
  }
}
```

---

### 反模式 2.5: content 配置不完整

**问题**：tailwind.config.js 的 content 未覆盖所有文件，导致样式丢失。

**检测**：
```bash
# 检查 content 配置
grep -A10 "content:" tailwind.config.* 2>/dev/null

# 检查是否覆盖所有目录
ls src/components src/pages src/features 2>/dev/null | head -5
```

**修正**：
```js
// ❌ 错误：遗漏目录
module.exports = {
  content: ['./src/pages/**/*.tsx'],  // 遗漏 components
}

// ✅ 正确：完整覆盖
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 cn 工具函数（必备）

```tsx
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 使用
<div className={cn(
  'base-styles',
  isActive && 'active-styles',
  variant === 'primary' && 'primary-styles'
)} />
```

### 3.2 cva 组件变体（推荐）

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const button = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3 text-sm',
        lg: 'h-11 px-8 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

interface ButtonProps extends VariantProps<typeof button> {
  className?: string;
  children: React.ReactNode;
}

export function Button({ variant, size, className, children }: ButtonProps) {
  return (
    <button className={cn(button({ variant, size }), className)}>
      {children}
    </button>
  );
}
```

### 3.3 响应式设计（Mobile-First）

```tsx
// 响应式网格
<div className="
  grid
  grid-cols-1      /* 默认：1 列 */
  sm:grid-cols-2   /* 640px+：2 列 */
  lg:grid-cols-3   /* 1024px+：3 列 */
  xl:grid-cols-4   /* 1280px+：4 列 */
  gap-4 sm:gap-6
">
  {items.map(item => <Card key={item.id} />)}
</div>

// 响应式容器
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  {/* 自适应边距 */}
</div>
```

### 3.4 暗色模式

```tsx
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // 或 'media'
}

// 组件使用
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
  border-gray-200 dark:border-gray-700
">
  自适应主题
</div>

// 切换按钮示例
function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  return (
    <button onClick={() => setDark(!dark)}>
      {dark ? '🌙' : '☀️'}
    </button>
  );
}
```

### 3.5 交互状态

```tsx
<button className="
  bg-blue-500 text-white
  hover:bg-blue-600
  focus:outline-none focus:ring-2 focus:ring-blue-300
  active:bg-blue-700
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200
">
  交互按钮
</button>

// group 状态（父悬停影响子元素）
<div className="group">
  <img className="group-hover:scale-105 transition" />
  <p className="group-hover:text-blue-500">悬停父元素时变化</p>
</div>

// peer 状态（同级元素联动）
<input className="peer" type="checkbox" />
<label className="peer-checked:text-blue-500">
  复选框选中时变化
</label>
```

### 3.6 tailwind.config.js 完整配置

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#3b82f6',
          600: '#2563eb',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## 4. 自我验证 (Self-Verification)

### TailwindCSS 合规审计脚本

```bash
#!/bin/bash
# tailwind-audit.sh - TailwindCSS 代码合规检查

echo "🎨 TailwindCSS 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测动态类名拼接
echo -e "\n🔍 检测动态类名..."
DYNAMIC_CLASS=$(grep -rn "className={\`.*\${" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

if [ "$DYNAMIC_CLASS" -gt 0 ]; then
    echo "❌ 发现动态类名拼接（无法被 purge）:"
    grep -rn "className={\`.*\${" src/ --include="*.tsx" 2>/dev/null | head -5
    ((ERRORS++))
else
    echo "✅ 无动态类名问题"
fi

# 2. 检测 tailwind-merge 使用
echo -e "\n🔄 检测类名合并工具..."
TW_MERGE=$(grep -rln "twMerge\|tailwind-merge\|cn(" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

if [ "$TW_MERGE" -eq 0 ]; then
    echo "⚠️ 未发现 tailwind-merge 使用"
else
    echo "✅ 已使用类名合并工具 ($TW_MERGE 个文件)"
fi

# 3. 检测类名冲突
echo -e "\n⚠️ 检测潜在类名冲突..."
CONFLICTS=$(grep -rn "className=" src/ --include="*.tsx" 2>/dev/null | \
  grep -c "p-[0-9].*p-[0-9]\|m-[0-9].*m-[0-9]" || echo "0")

if [ "$CONFLICTS" -gt 0 ]; then
    echo "⚠️ 发现潜在类名冲突 ($CONFLICTS 处)"
else
    echo "✅ 无明显类名冲突"
fi

# 4. 检测 content 配置
echo -e "\n📁 检测 content 配置..."
if [ -f "tailwind.config.js" ] || [ -f "tailwind.config.ts" ]; then
    CONTENT=$(grep -A5 "content:" tailwind.config.* 2>/dev/null)
    if [ -n "$CONTENT" ]; then
        echo "✅ content 已配置"
        echo "$CONTENT" | head -6
    else
        echo "❌ 未发现 content 配置"
        ((ERRORS++))
    fi
else
    echo "⚠️ 未发现 tailwind.config 文件"
fi

# 5. 检测暗色模式配置
echo -e "\n🌙 检测暗色模式..."
DARK_MODE=$(grep "darkMode" tailwind.config.* 2>/dev/null)

if [ -n "$DARK_MODE" ]; then
    echo "✅ 暗色模式已配置: $DARK_MODE"
else
    echo "⚠️ 未配置暗色模式策略"
fi

# 6. 检测 @apply 过度使用
echo -e "\n📝 检测 @apply 使用..."
APPLY_COUNT=$(grep -rn "@apply" src/ --include="*.css" 2>/dev/null | wc -l | tr -d ' ')

if [ "$APPLY_COUNT" -gt 20 ]; then
    echo "⚠️ @apply 使用过多 ($APPLY_COUNT 处)，考虑使用 cva"
else
    echo "✅ @apply 使用适度 ($APPLY_COUNT 处)"
fi

# 7. 检测 cva 使用（推荐）
echo -e "\n🧩 检测 cva 使用..."
CVA=$(grep -rln "class-variance-authority\|cva(" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

if [ "$CVA" -gt 0 ]; then
    echo "✅ 已使用 cva 组件变体 ($CVA 个文件)"
else
    echo "💡 建议：考虑使用 cva 管理组件变体"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ TailwindCSS 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 无动态类名拼接（使用映射对象或 cva）
- [ ] 使用 `cn()` 或 `twMerge()` 处理条件类名
- [ ] 响应式类名遵循 mobile-first（sm → md → lg → xl）
- [ ] `tailwind.config.js` content 覆盖所有源文件
- [ ] 配置了 `darkMode: 'class'` 策略
- [ ] `@apply` 仅用于高频复杂组件
- [ ] 考虑使用 `cva` 管理组件变体

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `shadcn-ui-patterns` | 基于 Tailwind + cva 的组件库 |
| `radix-ui-patterns` | 无障碍组件 + Tailwind 样式 |
| `h5-responsive` | 响应式断点策略 |
| `framer-motion-patterns` | 动画配合 transition 类 |

### 推荐工具链

- Tailwind CSS IntelliSense (VS Code)
- Prettier Plugin Tailwind CSS
- tailwind-merge + clsx
- class-variance-authority (cva)

### 关联文件

- `tailwind.config.js` / `tailwind.config.ts`
- `src/lib/utils.ts` (cn 函数)
- `postcss.config.js`

---

**✅ TailwindCSS Patterns v2.0.0** | **标准 4 Section 已集成**
