---
name: react-hook-form-patterns
description: |
  React Hook Form + Zod 表单最佳实践。当涉及表单验证、提交、错误处理时自动触发。
  关键词：react-hook-form、表单、form、validation、zod、schema、submit。
  【表单核心】包含验证、错误处理、性能优化。
version: 2.0.0
allowed-tools: Read, Grep, Glob
---

# React Hook Form 表单模式

## 项目架构

```
src/components/
├── forms/
│   ├── FormField.tsx         # 通用表单字段封装
│   └── FormWrapper.tsx       # 表单容器组件
├── hooks/
│   └── useFormWithSchema.ts  # 带 Schema 的表单 Hook
└── schemas/
    └── userSchema.ts         # Zod Schema 定义

技术栈：
- React Hook Form 7.x
- Zod 3.x
- @hookform/resolvers
```

---

## 1. 硬性约束 (Hard Constraints)

### 配置约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 必须使用 zodResolver | 类型安全验证 | `grep -rln "useForm" src/ --include="*.tsx" \| xargs grep -L "zodResolver"` | 🔴 Critical |
| 数字字段必须 valueAsNumber | 避免字符串类型错误 | `grep -rn "type=\"number\"" src/ --include="*.tsx" \| xargs grep -v "valueAsNumber"` | 🔴 Critical |
| 必须处理 isSubmitting 状态 | 防止重复提交 | `grep -rln "handleSubmit" src/ --include="*.tsx" \| xargs grep -L "isSubmitting\|disabled"` | 🟡 Warning |
| 异步数据必须用 reset | 不能直接 defaultValues | `grep -rn "defaultValues.*fetch\|defaultValues.*async" src/ --include="*.tsx"` | 🔴 Critical |

### 性能约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 禁止 watch() 无参数调用 | 避免整表单订阅 | `grep -rn "watch()" src/ --include="*.tsx" \| grep -v "watch('.*')"` | 🔴 Critical |
| Controller 必须有 control | 否则不受控 | `grep -A5 "Controller" src/ --include="*.tsx" \| grep -v "control="` | 🔴 Critical |
| useFieldArray 必须用 field.id 作 key | 避免重渲染问题 | `grep -A10 "useFieldArray" src/ --include="*.tsx" \| grep "key={index}"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 忘记 valueAsNumber

**问题**：`<input type="number">` 默认返回字符串，导致 Zod 验证失败或类型错误。

**检测**：
```bash
# 检测数字输入缺少 valueAsNumber
grep -rn "type=\"number\"" src/ --include="*.tsx" | \
  xargs grep -v "valueAsNumber"

# 检测 register 数字字段
grep -rn "register('.*')" src/ --include="*.tsx" | \
  grep -B2 "type=\"number\"" | \
  grep -v "valueAsNumber"
```

**修正**：
```typescript
// ❌ 错误：age 是字符串 "18"
<input type="number" {...register('age')} />

// ✅ 正确：age 是数字 18
<input type="number" {...register('age', { valueAsNumber: true })} />

// ✅ 或在 Schema 中转换
const schema = z.object({
  age: z.coerce.number().min(18),  // 自动转换
});
```

---

### 反模式 2.2: 异步数据直接设 defaultValues

**问题**：defaultValues 只在初始化时生效，异步获取的数据不会更新表单。

**检测**：
```bash
# 检测 defaultValues 使用异步数据
grep -rn "defaultValues:" src/ --include="*.tsx" -A3 | \
  grep "fetch\|async\|await\|data\?"

# 检测缺少 reset 调用
grep -rln "useForm" src/ --include="*.tsx" | \
  xargs grep -L "reset("
```

**修正**：
```typescript
// ❌ 错误：fetchedData 可能还没到
const { register } = useForm({
  defaultValues: fetchedData,  // 初始化时 fetchedData 是 undefined
});

// ✅ 正确：使用 reset 更新
const { register, reset } = useForm({
  defaultValues: { name: '', email: '' },  // 初始默认值
});

useEffect(() => {
  if (fetchedData) {
    reset(fetchedData);  // 数据到达后重置表单
  }
}, [fetchedData, reset]);
```

---

### 反模式 2.3: watch() 全表单订阅

**问题**：无参数调用 watch() 订阅整个表单，任何字段变化都触发重渲染。

**检测**：
```bash
# 检测 watch() 无参数调用
grep -rn "watch()" src/ --include="*.tsx" | grep -v "watch('.*')"

# 检测解构 watch 返回值
grep -rn "const.*=.*watch()" src/ --include="*.tsx"
```

**修正**：
```typescript
// ❌ 错误：订阅所有字段
const formData = watch();  // 任何变化都重渲染

// ✅ 正确：只订阅需要的字段
const name = watch('name');

// ✅ 正确：订阅多个特定字段
const [name, email] = watch(['name', 'email']);

// ✅ 正确：使用 useWatch 优化
import { useWatch } from 'react-hook-form';
const name = useWatch({ control, name: 'name' });
```

---

### 反模式 2.4: Controller 缺少 control

**问题**：Controller 没有传入 control，组件不受表单控制。

**检测**：
```bash
# 检测 Controller 缺少 control
grep -A5 "<Controller" src/ -r --include="*.tsx" | \
  grep -B3 "/>" | \
  grep -v "control="
```

**修正**：
```typescript
// ❌ 错误：缺少 control
<Controller
  name="select"
  render={({ field }) => <Select {...field} />}
/>

// ✅ 正确：传入 control
const { control } = useForm();

<Controller
  name="select"
  control={control}  // ⚠️ 必须传入
  render={({ field }) => <Select {...field} />}
/>
```

---

### 反模式 2.5: useFieldArray 用 index 作 key

**问题**：使用 index 作为 key，删除/添加时会导致状态错乱。

**检测**：
```bash
# 检测 useFieldArray 使用 index 作 key
grep -A15 "useFieldArray" src/ -r --include="*.tsx" | \
  grep "key={index}"

# 检测未使用 field.id
grep -A15 "fields.map" src/ -r --include="*.tsx" | \
  grep -v "field.id"
```

**修正**：
```typescript
// ❌ 错误：用 index 作 key
{fields.map((field, index) => (
  <div key={index}>  {/* 💥 删除时状态错乱 */}
    <input {...register(`items.${index}.name`)} />
  </div>
))}

// ✅ 正确：用 field.id 作 key
{fields.map((field, index) => (
  <div key={field.id}>  {/* ✅ React Hook Form 生成的稳定 ID */}
    <input {...register(`items.${index}.name`)} />
  </div>
))}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 基础表单 + Zod 验证

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2, '名称至少 2 个字符'),
  email: z.string().email('邮箱格式不正确'),
  age: z.number().min(18, '必须年满 18 岁'),
});

type FormData = z.infer<typeof schema>;

function MyForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      name: '',
      email: '',
      age: 18,
    },
  });

  const onSubmit = async (data: FormData) => {
    await api.submit(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '提交中...' : '提交'}
      </button>
    </form>
  );
}
```

### 3.2 与 Ant Design 集成

```typescript
import { Form, Input, Button, message } from 'antd';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  name: z.string().min(1, '请输入名称'),
  email: z.string().email('邮箱格式不正确'),
});

function AntdForm() {
  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data) => {
    try {
      await api.submit(data);
      message.success('提交成功');
    } catch (error) {
      message.error('提交失败');
    }
  };

  return (
    <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
      <Form.Item
        label="名称"
        validateStatus={errors.name ? 'error' : ''}
        help={errors.name?.message}
      >
        <Controller
          name="name"
          control={control}
          render={({ field }) => <Input {...field} />}
        />
      </Form.Item>

      <Form.Item
        label="邮箱"
        validateStatus={errors.email ? 'error' : ''}
        help={errors.email?.message}
      >
        <Controller
          name="email"
          control={control}
          render={({ field }) => <Input {...field} />}
        />
      </Form.Item>

      <Button type="primary" htmlType="submit" loading={isSubmitting}>
        提交
      </Button>
    </Form>
  );
}
```

### 3.3 动态字段 (useFieldArray)

```typescript
import { useForm, useFieldArray } from 'react-hook-form';

const schema = z.object({
  items: z.array(z.object({
    name: z.string().min(1),
    quantity: z.number().min(1),
  })).min(1, '至少添加一项'),
});

function DynamicForm() {
  const { control, register, handleSubmit } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { items: [{ name: '', quantity: 1 }] },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>  {/* ⚠️ 必须用 field.id */}
          <input {...register(`items.${index}.name`)} />
          <input
            type="number"
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
          />
          <button type="button" onClick={() => remove(index)}>
            删除
          </button>
        </div>
      ))}
      <button type="button" onClick={() => append({ name: '', quantity: 1 })}>
        添加
      </button>
      <button type="submit">提交</button>
    </form>
  );
}
```

### 3.4 异步数据加载

```typescript
function EditForm({ id }: { id: string }) {
  const { data, isLoading } = useQuery(['item', id], () => api.getItem(id));

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting, isDirty },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      name: '',
      description: '',
    },
  });

  // 数据加载后重置表单
  useEffect(() => {
    if (data) {
      reset(data);
    }
  }, [data, reset]);

  if (isLoading) return <Skeleton />;

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* 表单字段 */}
      <button type="submit" disabled={isSubmitting || !isDirty}>
        保存
      </button>
    </form>
  );
}
```

### 3.5 性能优化

```typescript
import { useForm, useWatch, useFormContext } from 'react-hook-form';

// 1. 使用 useWatch 替代 watch
function WatchedField() {
  const { control } = useFormContext();
  const name = useWatch({ control, name: 'name' });

  return <div>当前值: {name}</div>;
}

// 2. 使用 FormProvider 避免 prop drilling
function FormWithContext() {
  const methods = useForm();

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <NestedField />
        <WatchedField />
      </form>
    </FormProvider>
  );
}

function NestedField() {
  const { register } = useFormContext();
  return <input {...register('nested.field')} />;
}
```

---

## 4. 自我验证 (Self-Verification)

### React Hook Form 合规审计脚本

```bash
#!/bin/bash
# rhf-audit.sh - React Hook Form 代码合规检查

echo "📝 React Hook Form 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测缺少 zodResolver
echo -e "\n🔍 检测 Schema 验证..."
FORM_FILES=$(grep -rln "useForm" src/ --include="*.tsx" 2>/dev/null)
MISSING_RESOLVER=""

for file in $FORM_FILES; do
    if ! grep -q "zodResolver\|yupResolver" "$file" 2>/dev/null; then
        MISSING_RESOLVER="$MISSING_RESOLVER\n  - $file"
    fi
done

if [ -n "$MISSING_RESOLVER" ]; then
    echo "❌ 以下表单缺少 Schema 验证:$MISSING_RESOLVER"
    ((ERRORS++))
else
    echo "✅ 所有表单都使用了 Schema 验证"
fi

# 2. 检测数字字段缺少 valueAsNumber
echo -e "\n🔢 检测数字字段..."
NUMBER_ISSUE=$(grep -rn "type=\"number\"" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "valueAsNumber" | head -5)

if [ -n "$NUMBER_ISSUE" ]; then
    echo "❌ 数字字段缺少 valueAsNumber:"
    echo "$NUMBER_ISSUE"
    ((ERRORS++))
else
    echo "✅ 数字字段处理正确"
fi

# 3. 检测 watch() 无参数调用
echo -e "\n👀 检测 watch 使用..."
WATCH_ALL=$(grep -rn "watch()" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "watch('.*')" | head -5)

if [ -n "$WATCH_ALL" ]; then
    echo "❌ 发现 watch() 全表单订阅:"
    echo "$WATCH_ALL"
    ((ERRORS++))
else
    echo "✅ watch 使用正确"
fi

# 4. 检测 Controller 缺少 control
echo -e "\n🎮 检测 Controller 配置..."
CONTROLLER_FILES=$(grep -rln "Controller" src/ --include="*.tsx" 2>/dev/null)
MISSING_CONTROL=""

for file in $CONTROLLER_FILES; do
    # 检测有 Controller 但无 control=
    if grep -q "<Controller" "$file" 2>/dev/null; then
        if ! grep -A5 "<Controller" "$file" 2>/dev/null | grep -q "control="; then
            MISSING_CONTROL="$MISSING_CONTROL\n  - $file"
        fi
    fi
done

if [ -n "$MISSING_CONTROL" ]; then
    echo "⚠️ Controller 可能缺少 control:$MISSING_CONTROL"
else
    echo "✅ Controller 配置正确"
fi

# 5. 检测 useFieldArray 的 key
echo -e "\n🔄 检测动态字段..."
FIELD_ARRAY_FILES=$(grep -rln "useFieldArray" src/ --include="*.tsx" 2>/dev/null)
BAD_KEY=""

for file in $FIELD_ARRAY_FILES; do
    if grep -A15 "fields.map" "$file" 2>/dev/null | grep -q "key={index}"; then
        BAD_KEY="$BAD_KEY\n  - $file"
    fi
done

if [ -n "$BAD_KEY" ]; then
    echo "❌ useFieldArray 使用 index 作 key:$BAD_KEY"
    ((ERRORS++))
else
    if [ -n "$FIELD_ARRAY_FILES" ]; then
        echo "✅ useFieldArray key 使用正确"
    else
        echo "ℹ️ 未使用 useFieldArray"
    fi
fi

# 6. 检测 isSubmitting 处理
echo -e "\n⏳ 检测提交状态..."
SUBMIT_FILES=$(grep -rln "handleSubmit" src/ --include="*.tsx" 2>/dev/null)
MISSING_SUBMIT_STATE=""

for file in $SUBMIT_FILES; do
    if ! grep -q "isSubmitting\|disabled.*submit" "$file" 2>/dev/null; then
        MISSING_SUBMIT_STATE="$MISSING_SUBMIT_STATE\n  - $file"
    fi
done

if [ -n "$MISSING_SUBMIT_STATE" ]; then
    echo "⚠️ 以下表单可能未处理提交状态:$MISSING_SUBMIT_STATE"
else
    echo "✅ 提交状态处理正确"
fi

# 7. 检测 reset 使用
echo -e "\n🔄 检测异步数据处理..."
ASYNC_DEFAULT=$(grep -rn "defaultValues:" src/ --include="*.tsx" -A3 2>/dev/null | \
  grep "fetch\|async\|data\?" | head -3)

if [ -n "$ASYNC_DEFAULT" ]; then
    echo "⚠️ 发现可能的异步 defaultValues:"
    echo "$ASYNC_DEFAULT"
    echo "  建议使用 reset() 更新"
else
    echo "✅ 未发现异步 defaultValues 问题"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ React Hook Form 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 所有表单使用 `zodResolver` 进行类型安全验证
- [ ] 数字输入使用 `valueAsNumber: true`
- [ ] 异步数据使用 `reset()` 而非 `defaultValues`
- [ ] `watch()` 只订阅需要的字段，不全表单订阅
- [ ] `Controller` 组件传入 `control` 属性
- [ ] `useFieldArray` 使用 `field.id` 作为 key
- [ ] 提交按钮根据 `isSubmitting` 禁用

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `zustand-patterns` | 表单状态持久化 |
| `react-query-patterns` | 表单数据获取和提交 |
| `radix-ui-patterns` | 表单组件样式和无障碍 |
| `shadcn-ui-patterns` | Form 组件集成 |

### 关联文件

- `src/components/forms/*.tsx`
- `src/schemas/*.ts`
- `src/hooks/useFormWithSchema.ts`

---

**✅ React Hook Form Patterns v2.0.0** | **标准 4 Section 已集成**
