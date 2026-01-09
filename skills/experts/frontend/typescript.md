## TypeScript 生产级标准

> 基于 [TypeScript 官方文档](https://www.typescriptlang.org/docs/)、[Matt Pocock 教程](https://www.totaltypescript.com/)、[Type Challenges](https://github.com/type-challenges/type-challenges)

### 🔴 强制要求（不可妥协）

| 维度 | 要求 | 验证方式 |
|------|------|---------|
| **strict 模式** | `tsconfig.json` 必须启用 strict | 配置审查 |
| **零 any** | 禁止使用 any，使用 unknown 代替 | `tsc --noEmit` |
| **显式返回类型** | 公共 API 函数必须声明返回类型 | 代码审查 |
| **null 安全** | 启用 strictNullChecks，显式处理 null | 编译检查 |
| **类型守卫** | 运行时类型检查使用类型守卫 | 代码审查 |

### 🟡 质量标准

| 维度 | 标准 |
|------|------|
| **类型推断** | 优先利用推断，避免冗余类型注解 |
| **泛型约束** | 泛型使用 extends 约束，避免过于宽松 |
| **工具类型** | 优先使用内置工具类型 (Partial, Pick, Omit 等) |
| **类型文档** | 复杂类型添加 JSDoc 注释 |

### ❌ 禁止行为

- 禁止 `// @ts-ignore` 或 `// @ts-expect-error`（除非有充分理由）
- 禁止 `as any` 类型断言
- 禁止 `!` 非空断言（除非 100% 确定）
- 禁止空 interface（使用 type 别名）
- 禁止 `Function` 类型（使用具体函数签名）

---

## 🚨 TypeScript 生产级陷阱（必须掌握）

### 陷阱 1: any 类型传染 ⭐⭐⭐⭐⭐

**现象**: 类型错误被静默吞没，运行时才暴露问题

**根因**: any 类型会"传染"给所有关联变量，禁用类型检查

```typescript
// ❌ 错误写法 - any 传染
function parseData(data: any) {
  return data.items.map((item: any) => item.name);  // 全是 any！
}
const result = parseData(response);  // result 是 any
result.nonExistent.method();  // 编译通过，运行时崩溃！

// ✅ 正确写法 - 使用 unknown + 类型守卫
function parseData(data: unknown): string[] {
  if (!isValidResponse(data)) {
    throw new Error('Invalid data format');
  }
  return data.items.map(item => item.name);
}

// 类型守卫
function isValidResponse(data: unknown): data is { items: { name: string }[] } {
  return (
    typeof data === 'object' &&
    data !== null &&
    'items' in data &&
    Array.isArray((data as any).items)
  );
}
```

### 陷阱 2: 类型断言滥用 ⭐⭐⭐⭐⭐

**现象**: 类型断言后运行时类型不匹配

**根因**: `as` 断言只骗过编译器，不改变运行时值

```typescript
// ❌ 错误写法 - 断言不等于转换
interface User {
  id: number;
  name: string;
  email: string;
}

const data = JSON.parse(response) as User;  // 危险！
console.log(data.email.toLowerCase());  // 如果 email 是 undefined 会崩溃

// ✅ 正确写法 - 验证后再断言
function parseUser(data: unknown): User {
  if (
    typeof data === 'object' &&
    data !== null &&
    typeof (data as any).id === 'number' &&
    typeof (data as any).name === 'string' &&
    typeof (data as any).email === 'string'
  ) {
    return data as User;
  }
  throw new Error('Invalid user data');
}

// ✅ 更佳 - 使用 Zod 等验证库
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;
const user = UserSchema.parse(data);  // 运行时验证 + 类型推断
```

### 陷阱 3: 对象字面量多余属性检查绕过 ⭐⭐⭐⭐

**现象**: 多余属性被静默忽略，数据不一致

**根因**: TypeScript 只对字面量做多余属性检查，变量赋值会绕过

```typescript
interface Config {
  host: string;
  port: number;
}

// ✅ 字面量 - 会报错
const config1: Config = {
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // ❌ Error: 'timeout' does not exist in type 'Config'
};

// ❌ 变量赋值 - 不报错！
const rawConfig = {
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // 静默通过！
};
const config2: Config = rawConfig;  // 编译通过，timeout 被忽略

// ✅ 正确写法 - 使用 satisfies
const config3 = {
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // ❌ Error with satisfies
} satisfies Config;

// ✅ 或使用函数包装
function createConfig(config: Config): Config {
  return config;
}
const config4 = createConfig({
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // ❌ Error
});
```

### 陷阱 4: 联合类型收窄不完整 ⭐⭐⭐⭐

**现象**: switch/if 遗漏分支，新增类型时无编译错误

**根因**: 未使用 exhaustive check（穷尽检查）

```typescript
type Status = 'pending' | 'success' | 'error';

// ❌ 错误写法 - 遗漏分支无警告
function getStatusMessage(status: Status): string {
  switch (status) {
    case 'pending':
      return 'Loading...';
    case 'success':
      return 'Done!';
    // 忘记处理 'error'，但编译通过！
  }
  return '';  // 隐式返回
}

// 后来新增 'cancelled' 状态，但这里不会报错！

// ✅ 正确写法 - exhaustive check
function getStatusMessage(status: Status): string {
  switch (status) {
    case 'pending':
      return 'Loading...';
    case 'success':
      return 'Done!';
    case 'error':
      return 'Failed!';
    default:
      // 穷尽检查：如果遗漏分支，这里会报类型错误
      const _exhaustive: never = status;
      throw new Error(`Unhandled status: ${_exhaustive}`);
  }
}
```

### 陷阱 5: 泛型约束过于宽松 ⭐⭐⭐⭐

**现象**: 泛型函数接受任意类型，失去类型安全

```typescript
// ❌ 错误写法 - 无约束泛型
function getProperty<T>(obj: T, key: string): any {
  return (obj as any)[key];  // 完全失去类型安全
}

// ✅ 正确写法 - 使用 keyof 约束
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'Alice', age: 30 };
getProperty(user, 'name');     // ✅ 返回类型是 string
getProperty(user, 'age');      // ✅ 返回类型是 number
getProperty(user, 'invalid');  // ❌ Error: 'invalid' 不是 keyof typeof user
```

### 陷阱 6: 可辨识联合类型使用不当 ⭐⭐⭐

**现象**: 类型收窄失败，需要多次断言

**根因**: 缺少共同的字面量类型字段

```typescript
// ❌ 错误写法 - 无法自动收窄
interface Dog {
  bark(): void;
}
interface Cat {
  meow(): void;
}
type Animal = Dog | Cat;

function makeSound(animal: Animal) {
  if ('bark' in animal) {
    animal.bark();  // 可以工作，但不够优雅
  }
}

// ✅ 正确写法 - 可辨识联合
interface Dog {
  kind: 'dog';  // 字面量类型作为判别字段
  bark(): void;
}
interface Cat {
  kind: 'cat';
  meow(): void;
}
type Animal = Dog | Cat;

function makeSound(animal: Animal) {
  switch (animal.kind) {
    case 'dog':
      animal.bark();  // 自动收窄为 Dog
      break;
    case 'cat':
      animal.meow();  // 自动收窄为 Cat
      break;
  }
}
```

### 陷阱 7: 函数重载顺序错误 ⭐⭐⭐

**现象**: 更具体的重载被更通用的覆盖

**根因**: TypeScript 按顺序匹配重载，第一个匹配的生效

```typescript
// ❌ 错误写法 - 顺序错误
function processValue(value: string | number): string;  // 通用
function processValue(value: string): string;  // 具体
function processValue(value: string | number) {
  return String(value);
}

processValue('hello');  // 匹配第一个重载，不是第二个！

// ✅ 正确写法 - 从具体到通用
function processValue(value: string): string;  // 最具体
function processValue(value: number): string;  // 次具体
function processValue(value: string | number): string;  // 最通用
function processValue(value: string | number) {
  return String(value);
}
```

### 陷阱 8: const assertion 遗忘 ⭐⭐⭐

**现象**: 对象/数组类型被推断为可变类型

```typescript
// ❌ 问题 - 类型被扩展
const config = {
  endpoint: '/api/users',
  method: 'GET',
};
// 类型是 { endpoint: string; method: string }
// 而不是 { endpoint: '/api/users'; method: 'GET' }

function fetchData(config: { endpoint: string; method: 'GET' | 'POST' }) {
  // ...
}
fetchData(config);  // ❌ Error: method 是 string，不是 'GET' | 'POST'

// ✅ 正确写法 - as const
const config = {
  endpoint: '/api/users',
  method: 'GET',
} as const;
// 类型是 { readonly endpoint: '/api/users'; readonly method: 'GET' }

fetchData(config);  // ✅ 正常工作
```

---

## 🔧 常用工具类型速查

### 内置工具类型

| 类型 | 作用 | 示例 |
|------|------|------|
| `Partial<T>` | 所有属性可选 | `Partial<User>` |
| `Required<T>` | 所有属性必选 | `Required<Config>` |
| `Readonly<T>` | 所有属性只读 | `Readonly<State>` |
| `Pick<T, K>` | 选取部分属性 | `Pick<User, 'id' \| 'name'>` |
| `Omit<T, K>` | 排除部分属性 | `Omit<User, 'password'>` |
| `Record<K, V>` | 键值对类型 | `Record<string, number>` |
| `Exclude<T, U>` | 从联合中排除 | `Exclude<Status, 'error'>` |
| `Extract<T, U>` | 从联合中提取 | `Extract<Status, 'success'>` |
| `NonNullable<T>` | 排除 null/undefined | `NonNullable<string \| null>` |
| `ReturnType<T>` | 函数返回类型 | `ReturnType<typeof fn>` |
| `Parameters<T>` | 函数参数类型 | `Parameters<typeof fn>` |

### 自定义工具类型

```typescript
// DeepPartial - 深度可选
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// DeepReadonly - 深度只读
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Nullable - 允许 null
type Nullable<T> = T | null;

// ValueOf - 对象值类型
type ValueOf<T> = T[keyof T];
```

---

## ✅ tsconfig.json 生产配置

```json
{
  "compilerOptions": {
    // 严格模式（必须）
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // 额外检查
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,

    // 模块解析
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "isolatedModules": true,

    // 输出
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

---

## ✅ 交付检查清单

```
□ tsconfig.json strict: true 已启用
□ 零 any 类型（使用 unknown + 类型守卫）
□ 公共函数有显式返回类型
□ 联合类型有 exhaustive check
□ 外部数据使用 Zod 等验证
□ 复杂类型有 JSDoc 注释
□ 泛型有适当的约束 (extends)
□ 无 @ts-ignore 或 @ts-expect-error
□ 使用 as const 保持字面量类型
```

### 📋 类型设计检查

| 检查项 | 说明 |
|--------|------|
| **类型完整性** | 所有数据结构有对应类型定义 |
| **类型一致性** | 前后端共享类型定义（或生成） |
| **类型安全性** | 无隐式 any，无不安全断言 |
| **类型可读性** | 复杂类型有注释和示例 |
```
