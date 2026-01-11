---
name: shadcn-ui-patterns
description: |
  shadcn/ui 组件库专家 - Radix、可访问性组件。
  Use when:
  - 使用 shadcn/ui 组件
  - Radix UI、headless 组件
  - 可访问性、主题定制
  触发词：shadcn、Radix、headless、accessible、cn、cva
  Related Skills: tailwindcss-patterns, react-hook-form-patterns, framer-motion-patterns
allowed-tools: Read, Grep, Glob
---

# shadcn/ui 组件库

## 核心理念

### 非传统组件库

```
传统组件库：npm install → import → 配置受限
shadcn/ui：npx shadcn-ui add → 复制到项目 → 完全可控
```

### 架构基础

| 层次 | 技术 | 职责 |
|------|------|------|
| 底层 | Radix UI | 无样式、可访问性原语 |
| 样式 | Tailwind CSS | 原子化样式系统 |
| 变体 | class-variance-authority | 组件变体管理 |
| 工具 | clsx + tailwind-merge | 类名合并 |

## 初始化配置

### 项目初始化

```bash
npx shadcn-ui@latest init

# 配置选项
# - TypeScript: Yes
# - Style: Default / New York
# - Base color: Slate / Gray / Zinc / Neutral / Stone
# - CSS variables: Yes
# - tailwind.config.js location
# - components.json 配置文件
```

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

## cn 工具函数

### 核心实现

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 使用场景

```tsx
import { cn } from '@/lib/utils';

// 条件类名
<div className={cn(
  'base-class',
  isActive && 'active-class',
  variant === 'primary' && 'primary-class'
)} />

// 合并外部类名
interface ButtonProps {
  className?: string;
}

function Button({ className, ...props }: ButtonProps) {
  return (
    <button
      className={cn('default-styles', className)}
      {...props}
    />
  );
}
```

## 组件添加与定制

### 添加组件

```bash
# 添加单个组件
npx shadcn-ui@latest add button

# 添加多个组件
npx shadcn-ui@latest add button card dialog

# 查看所有可用组件
npx shadcn-ui@latest add
```

### 组件定制

```tsx
// components/ui/button.tsx (生成后可自由修改)
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

## 主题系统

### CSS 变量

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... 暗色模式变量 */
  }
}
```

### 主题切换

```tsx
// 使用 next-themes
import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

// 主题切换组件
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

## 表单处理

### React Hook Form + Zod

```tsx
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const formSchema = z.object({
  username: z.string().min(2, {
    message: '用户名至少2个字符',
  }),
  email: z.string().email({
    message: '请输入有效的邮箱地址',
  }),
});

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: '',
      email: '',
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>用户名</FormLabel>
              <FormControl>
                <Input placeholder="输入用户名" {...field} />
              </FormControl>
              <FormDescription>这是你的公开显示名称</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">提交</Button>
      </form>
    </Form>
  );
}
```

## 常用组件模式

### Dialog 对话框

```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

export function EditDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">编辑资料</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>编辑资料</DialogTitle>
          <DialogDescription>
            修改你的个人信息，完成后点击保存。
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {/* 表单内容 */}
        </div>
        <DialogFooter>
          <Button type="submit">保存</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

### Command 命令面板

```tsx
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';

export function CommandMenu() {
  const [open, setOpen] = React.useState(false);

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="搜索..." />
      <CommandList>
        <CommandEmpty>未找到结果</CommandEmpty>
        <CommandGroup heading="建议">
          <CommandItem>日历</CommandItem>
          <CommandItem>搜索表情</CommandItem>
          <CommandItem>计算器</CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
```

### DataTable 数据表格

```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

// 配合 @tanstack/react-table 使用
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <Table>
      <TableHeader>
        {table.getHeaderGroups().map((headerGroup) => (
          <TableRow key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <TableHead key={header.id}>
                {flexRender(
                  header.column.columnDef.header,
                  header.getContext()
                )}
              </TableHead>
            ))}
          </TableRow>
        ))}
      </TableHeader>
      <TableBody>
        {table.getRowModel().rows.map((row) => (
          <TableRow key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

## 可访问性

### 键盘导航

```tsx
// Radix UI 自动处理：
// - Dialog: Escape 关闭, Tab 焦点陷阱
// - DropdownMenu: 方向键导航, Enter 选择
// - Tabs: 方向键切换
```

### 屏幕阅读器

```tsx
// 使用语义化标签
<DialogTitle>标题会被读取</DialogTitle>
<DialogDescription>描述会被读取</DialogDescription>

// aria 属性自动添加
// - aria-expanded
// - aria-selected
// - aria-labelledby
```

## 常见陷阱

### ❌ 陷阱 1：直接修改 node_modules

```bash
# ❌ 错误：修改依赖包
node_modules/@radix-ui/...

# ✅ 正确：组件在项目中，直接修改
components/ui/button.tsx
```

### ❌ 陷阱 2：忘记安装依赖

```bash
# 添加组件时会提示依赖
npx shadcn-ui add dialog
# 需要: @radix-ui/react-dialog

# 确保安装
pnpm add @radix-ui/react-dialog
```

### ❌ 陷阱 3：类名覆盖失效

```tsx
// ❌ 错误：样式不生效
<Button className="bg-red-500" /> // 可能被默认样式覆盖

// ✅ 正确：cn 函数合并
// Button 组件内部使用 cn(buttonVariants(), className)
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `tailwindcss-patterns` | 样式基础 |
| `react-patterns` | React 组件模式 |
| `zustand-patterns` | 状态管理集成 |

### 推荐工具链

- shadcn/ui CLI
- Radix UI
- class-variance-authority
- tailwind-merge
- lucide-react (图标)
- react-hook-form + zod
- @tanstack/react-table
