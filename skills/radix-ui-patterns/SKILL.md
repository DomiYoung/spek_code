---
name: radix-ui-patterns
description: |
  Radix UI 无障碍组件最佳实践。当涉及 Dialog、Dropdown、Tooltip 等组件时自动触发。
  关键词：radix、dialog、dropdown、tooltip、popover、无障碍、a11y。
  【UI 核心】包含无障碍、组合模式、样式定制。
version: 2.0.0
allowed-tools: Read, Grep, Glob
---

# Radix UI 组件模式

## 核心理念

Radix UI 是无样式的无障碍组件库，提供行为和无障碍，样式由你控制。

---

## 1. 硬性约束 (Hard Constraints)

### 组件结构约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| Trigger 必须使用 asChild | 避免多余 DOM 节点 | `grep -rn "<.*\.Trigger>" src/ --include="*.tsx" \| grep -v "asChild"` | 🔴 Critical |
| Content 必须包装在 Portal | 避免 overflow 裁剪 | `grep -B3 "\.Content" src/ --include="*.tsx" \| grep -v "Portal"` | 🔴 Critical |
| Dialog 必须有 Title | 无障碍要求 | `grep -A10 "Dialog\.Content" src/ --include="*.tsx" \| grep -v "Dialog\.Title"` | 🟡 Warning |
| Tooltip 必须有 Provider | 全局配置共享 | `grep -rn "Tooltip\.Root" src/ --include="*.tsx" \| xargs grep -L "Tooltip\.Provider"` | 🟡 Warning |

### 无障碍约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| Dialog 必须有 Description 或 aria-describedby | 屏幕阅读器支持 | 手动检查 Dialog.Content 内部 | 🟡 Warning |
| 禁用元素不能作为 Trigger | 无法获取焦点 | `grep -A3 "\.Trigger" src/ --include="*.tsx" \| grep "disabled"` | 🔴 Critical |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 忘记 asChild

**问题**：Trigger 内直接放置子元素但未使用 asChild，导致多余 DOM 节点。

**检测**：
```bash
# 检测 Trigger 内有子元素但无 asChild
grep -A3 "<.*\.Trigger>" src/ -r --include="*.tsx" | \
  grep -B1 "<button\|<a\|<div" | \
  grep -v "asChild"
```

**修正**：
```typescript
// ❌ 错误：多余的 DOM 节点（渲染 button > button）
<Dialog.Trigger>
  <button>打开</button>
</Dialog.Trigger>

// ✅ 正确：使用 asChild 合并属性
<Dialog.Trigger asChild>
  <button>打开</button>
</Dialog.Trigger>
```

---

### 反模式 2.2: 缺少 Portal

**问题**：Content 未包装在 Portal 中，被父容器 overflow 裁剪。

**检测**：
```bash
# 检测 Content 前是否有 Portal
grep -B5 "Dialog\.Content\|Dropdown.*\.Content\|Popover\.Content" src/ -r --include="*.tsx" | \
  grep -v "Portal"
```

**修正**：
```typescript
// ❌ 错误：Content 可能被裁剪
<div style={{ overflow: 'hidden' }}>
  <Dialog.Content>内容</Dialog.Content>
</div>

// ✅ 正确：使用 Portal 渲染到 body
<Dialog.Portal>
  <Dialog.Overlay className="overlay" />
  <Dialog.Content>内容</Dialog.Content>
</Dialog.Portal>
```

---

### 反模式 2.3: 缺少 Title

**问题**：Dialog 没有 Title，屏幕阅读器无法正确识别对话框。

**检测**：
```bash
# 检测 Dialog.Content 但无 Dialog.Title
grep -A15 "Dialog\.Content" src/ -r --include="*.tsx" | \
  grep -B10 "</Dialog.Content>" | \
  grep -v "Dialog\.Title"
```

**修正**：
```typescript
// ❌ 错误：缺少 Title，无障碍不完整
<Dialog.Content>
  <div>内容</div>
</Dialog.Content>

// ✅ 正确：添加 Title（可视觉隐藏）
<Dialog.Content>
  <Dialog.Title>对话框标题</Dialog.Title>
  <Dialog.Description>描述内容</Dialog.Description>
  <div>内容</div>
</Dialog.Content>

// ✅ 或者：视觉隐藏 Title
<Dialog.Content aria-describedby={undefined}>
  <VisuallyHidden>
    <Dialog.Title>确认删除</Dialog.Title>
  </VisuallyHidden>
  <div>内容</div>
</Dialog.Content>
```

---

### 反模式 2.4: Tooltip 无 Provider

**问题**：每个 Tooltip 独立配置，无法全局控制延迟等参数。

**检测**：
```bash
# 检测使用 Tooltip.Root 但无 Provider 包装
grep -rln "Tooltip\.Root" src/ --include="*.tsx" | \
  xargs grep -L "Tooltip\.Provider"
```

**修正**：
```typescript
// ❌ 错误：每个 Tooltip 独立，无法全局配置
function App() {
  return (
    <>
      <Tooltip.Root>...</Tooltip.Root>
      <Tooltip.Root>...</Tooltip.Root>
    </>
  );
}

// ✅ 正确：使用 Provider 包装
function App() {
  return (
    <Tooltip.Provider delayDuration={300} skipDelayDuration={100}>
      <Tooltip.Root>...</Tooltip.Root>
      <Tooltip.Root>...</Tooltip.Root>
    </Tooltip.Provider>
  );
}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 Dialog 完整模式

```typescript
import * as Dialog from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

export function MyDialog({
  trigger,
  title,
  description,
  children
}: DialogProps) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        {trigger}
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title className="dialog-title">
            {title}
          </Dialog.Title>

          {description && (
            <Dialog.Description className="dialog-description">
              {description}
            </Dialog.Description>
          )}

          {children}

          <Dialog.Close asChild>
            <button className="dialog-close" aria-label="关闭">
              <X />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### 3.2 Dropdown Menu 完整模式

```typescript
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

export function ActionMenu({ items }: { items: MenuItem[] }) {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button aria-label="更多操作">
          <MoreIcon />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="dropdown-content"
          sideOffset={5}
          align="end"
        >
          {items.map((item) => (
            <DropdownMenu.Item
              key={item.id}
              className="dropdown-item"
              onSelect={item.onSelect}
              disabled={item.disabled}
            >
              {item.icon && <span className="icon">{item.icon}</span>}
              {item.label}
              {item.shortcut && (
                <span className="shortcut">{item.shortcut}</span>
              )}
            </DropdownMenu.Item>
          ))}

          <DropdownMenu.Arrow className="dropdown-arrow" />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### 3.3 样式定制（data-state）

```css
/* 使用 data-state 属性控制动画 */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.dialog-overlay[data-state='open'] {
  animation: fadeIn 200ms ease-out;
}

.dialog-overlay[data-state='closed'] {
  animation: fadeOut 200ms ease-in;
}

.dialog-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 8px;
  padding: 24px;
  max-width: 450px;
  width: 90%;
}

.dialog-content[data-state='open'] {
  animation: scaleIn 200ms ease-out;
}

.dialog-content[data-state='closed'] {
  animation: scaleOut 200ms ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
  to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}
```

### 3.4 受控模式

```typescript
function ControlledDialog() {
  const [open, setOpen] = useState(false);

  const handleSubmit = async () => {
    await saveData();
    setOpen(false);  // 提交后关闭
  };

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button>打开</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          <form onSubmit={handleSubmit}>
            {/* 表单内容 */}
            <button type="submit">提交</button>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

## 4. 自我验证 (Self-Verification)

### Radix UI 合规审计脚本

```bash
#!/bin/bash
# radix-audit.sh - Radix UI 代码合规检查

echo "🎨 Radix UI 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测缺少 asChild
echo -e "\n🔘 检测 asChild 使用..."
MISSING_ASCHILD=$(grep -rn "<.*\.Trigger>" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "asChild" | head -5)

if [ -n "$MISSING_ASCHILD" ]; then
    echo "❌ Trigger 缺少 asChild:"
    echo "$MISSING_ASCHILD"
    ((ERRORS++))
else
    echo "✅ asChild 使用正常"
fi

# 2. 检测缺少 Portal
echo -e "\n📦 检测 Portal 使用..."
CONTENT_FILES=$(grep -rln "Dialog\.Content\|DropdownMenu\.Content" src/ --include="*.tsx" 2>/dev/null)
MISSING_PORTAL=""

for file in $CONTENT_FILES; do
    if ! grep -q "\.Portal" "$file" 2>/dev/null; then
        MISSING_PORTAL="$MISSING_PORTAL\n  - $file"
    fi
done

if [ -n "$MISSING_PORTAL" ]; then
    echo "❌ Content 缺少 Portal:$MISSING_PORTAL"
    ((ERRORS++))
else
    echo "✅ Portal 使用正常"
fi

# 3. 检测 Dialog 缺少 Title
echo -e "\n📝 检测 Dialog.Title..."
DIALOG_FILES=$(grep -rln "Dialog\.Content" src/ --include="*.tsx" 2>/dev/null)
MISSING_TITLE=""

for file in $DIALOG_FILES; do
    if ! grep -q "Dialog\.Title\|aria-labelledby" "$file" 2>/dev/null; then
        MISSING_TITLE="$MISSING_TITLE\n  - $file"
    fi
done

if [ -n "$MISSING_TITLE" ]; then
    echo "⚠️ Dialog 可能缺少 Title:$MISSING_TITLE"
else
    echo "✅ Dialog.Title 配置正常"
fi

# 4. 检测 Tooltip Provider
echo -e "\n💡 检测 Tooltip.Provider..."
TOOLTIP_FILES=$(grep -rln "Tooltip\.Root" src/ --include="*.tsx" 2>/dev/null)
MISSING_PROVIDER=""

for file in $TOOLTIP_FILES; do
    if ! grep -q "Tooltip\.Provider" "$file" 2>/dev/null; then
        MISSING_PROVIDER="$MISSING_PROVIDER\n  - $file"
    fi
done

if [ -n "$MISSING_PROVIDER" ]; then
    echo "⚠️ Tooltip 缺少 Provider:$MISSING_PROVIDER"
else
    echo "✅ Tooltip.Provider 配置正常"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ Radix UI 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 所有 `Trigger` 都使用了 `asChild`
- [ ] 所有 `Content` 都包装在 `Portal` 中
- [ ] 所有 `Dialog` 都有 `Title`（可视觉隐藏）
- [ ] `Tooltip` 使用 `Provider` 包装
- [ ] 使用 `data-state` 属性控制动画
- [ ] 受控模式正确处理 `open/onOpenChange`

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `shadcn-ui-patterns` | shadcn/ui 基于 Radix UI 构建 |
| `tailwindcss-patterns` | 样式定制配合 Tailwind |
| `framer-motion-patterns` | 复杂动画替代 CSS 动画 |

### 关联文件

- `src/components/ui/*.tsx`
- `src/components/dialogs/*.tsx`

---

**✅ Radix UI Patterns v2.0.0** | **标准 4 Section 已集成**
