---
name: code-quality-gates
type: Gate
version: 2.0.0
description: |
  代码质量强制门禁。当编写、修改、创建代码时自动触发。
  【强制执行】确保 Claude 遵守 CLAUDE.md 中的代码规范。
  关键词：写代码、创建组件、实现功能、修复Bug、编辑文件、添加函数。
  每次代码变更前后必须执行检查，违反红线立即停止。
allowed-tools: Read, Grep, Bash
---

# 代码质量门禁 (Code Quality Gates)

> **核心理念**：先读后写，先理解后修改，违反红线立即停止。
> **触发时机**：创建新文件、编辑代码、添加函数/组件、修复 Bug、重构。

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 立即停止，代码被拒绝

### 写代码前必须

| 规则 | 检查项 | 自动审计规则 |
|------|--------|-------------|
| **Read First** | 已读取目标文件 | 禁止直接 Write/Edit 未读过的文件 |
| **Pattern Check** | 已检查现有代码模式 | 使用 Serena 或 Grep 搜索 |
| **Understand First** | 理解现有代码结构再修改 | 代码审查验证 |

### 写代码时必须

| 规则 | 检查项 | 自动审计规则 |
|------|--------|-------------|
| **禁止裸 any** | `any` 必须有注释说明 | `grep -rn ": any" src/ --include="*.ts"` |
| **禁止 console.log** | 生产代码禁止 | `grep -rn "console.log" src/ --include="*.ts"` |
| **函数长度** | ≤ 50 行（警告）/ > 100 行（拒绝）| 代码行数统计 |
| **文件长度** | ≤ 500 行 | `wc -l src/**/*.tsx` |
| **嵌套深度** | ≤ 3 层 | 代码审查验证 |
| **useEffect 依赖** | 依赖数组完整 | ESLint react-hooks/exhaustive-deps |
| **错误处理** | 必须 try-catch / error boundary | 代码审查验证 |
| **状态不可变** | 禁止直接修改状态 | 使用 immer 或 spread |

### 写代码后必须

| 规则 | 检查项 | 自动审计规则 |
|------|--------|-------------|
| **类型检查** | TypeScript 无错误 | `pnpm exec tsc --noEmit` |
| **Lint 检查** | ESLint 无错误 | `pnpm lint` |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 裸 any 类型 ⭐⭐⭐⭐⭐

**问题**: 失去类型安全，运行时可能崩溃
**检测**: `grep -rn ": any" src/ --include="*.ts" --include="*.tsx"`
**修正**: 添加具体类型或注释说明原因

```typescript
// ❌ 禁止
const data: any = fetchData();
function process(input: any) {}

// ✅ 正确
const data: UserData = fetchData();
function process(input: ProcessInput): ProcessOutput {}

// ✅ 如果确实需要 any，必须注释
// TODO: API 返回类型待后端确认
const response: any = await api.get('/unknown');
```

### ❌ console.log 残留 ⭐⭐⭐⭐⭐

**问题**: 生产环境泄露敏感信息，影响性能
**检测**: `grep -rn "console.log" src/ --include="*.ts" --include="*.tsx"`
**修正**: 删除或替换为 logger

```typescript
// ❌ 禁止
console.log('user data:', user);

// ✅ 正确 - 删除或使用 logger
logger.debug('user data:', user);
```

### ❌ 函数过长 ⭐⭐⭐⭐

**问题**: 难以理解、测试、维护
**检测**: 函数行数 > 50 行
**修正**: 拆分为小函数，每个函数做一件事

```typescript
// ❌ 函数过长 (> 50 行)
function handleSubmit() {
  // ... 80 行代码
}

// ✅ 拆分为小函数
function handleSubmit() {
  const validated = validateForm();
  const formatted = formatData(validated);
  const result = submitToServer(formatted);
  handleResult(result);
}

function validateForm(): FormData { /* 15 行 */ }
function formatData(data: FormData): ApiPayload { /* 10 行 */ }
function submitToServer(payload: ApiPayload): Result { /* 10 行 */ }
function handleResult(result: Result): void { /* 10 行 */ }
```

### ❌ useEffect 依赖缺失 ⭐⭐⭐⭐

**问题**: 导致 stale closure，数据不同步
**检测**: ESLint react-hooks/exhaustive-deps 警告
**修正**: 添加完整依赖或使用 useCallback

```typescript
// ❌ 缺少依赖
useEffect(() => {
  fetchUser(userId);
}, []); // userId 未在依赖中

// ✅ 完整依赖
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ✅ 使用 useCallback 稳定引用
const handleFetch = useCallback(() => {
  fetchUser(userId);
}, [userId]);

useEffect(() => {
  handleFetch();
}, [handleFetch]);
```

### ❌ 直接修改状态 ⭐⭐⭐

**问题**: 破坏 React 响应式，导致渲染不更新
**检测**: 代码审查：`state.xxx = yyy` 模式
**修正**: 使用 immer 或 spread 操作符

```typescript
// ❌ 直接修改状态
state.items.push(newItem);
state.user.name = 'new name';

// ✅ 使用 immer（Zustand）
set((state) => {
  state.items.push(newItem);  // immer 允许
});

// ✅ 使用 spread
setItems([...items, newItem]);
setUser({ ...user, name: 'new name' });
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### 代码变更流程

```
1. Read 目标文件 → 理解现有结构
2. Grep/Serena 搜索 → 检查现有模式
3. 编写代码 → 遵循项目规范
4. tsc --noEmit → 类型检查通过
5. pnpm lint → Lint 检查通过
6. 提交代码 → review-quality-gates 最终审核
```

### 快速检查命令

```bash
# 完整检查（提交前必须运行）
pnpm lint && pnpm exec tsc --noEmit

# any 类型检查
grep -rn ": any" src/ --include="*.ts" --include="*.tsx"

# console.log 检查
grep -rn "console.log" src/ --include="*.ts" --include="*.tsx"

# 函数长度检查（手动）
grep -n "function\|const.*=.*(" src/**/*.tsx | head -50
```

### 警告阈值

| 维度 | 阈值 | 说明 |
|------|-----|------|
| 单次变更 | ≤ 200 行 | 超出考虑拆分 |
| PR 大小 | ≤ 500 行 | 超出必须拆分 |
| 新功能 | 需要测试 | 建议添加测试 |
| 复杂逻辑 | 需要注释 | 解释 WHY |

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前运行

### 检查失败处理

#### 🛑 红线违反

```
检测到红线违反！

❌ src/components/Chat.tsx:45
   函数 handleMessage 超过 100 行 (当前 127 行)

必须操作:
1. 立即停止当前操作
2. 拆分函数为多个小函数
3. 每个函数 ≤ 50 行
4. 重新执行检查

不允许继续，直到问题修复。
```

#### ⚠️ 警告

```
检测到警告项:

⚠️ src/stores/workflow.ts
   文件行数 487 行，接近 500 行限制

建议:
- 考虑拆分为多个模块
- 可以继续，但建议尽快重构
```

### 自动审计脚本

```bash
#!/bin/bash
# code-quality-audit.sh

echo "🔍 Code Quality Gates Audit..."

# 1. 检查 any 类型
ANY_COUNT=$(grep -rn ": any" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)
if [ "$ANY_COUNT" -gt 0 ]; then
  echo "❌ 发现 $ANY_COUNT 处裸 any 类型"
  grep -rn ": any" src/ --include="*.ts" --include="*.tsx"
  exit 1
fi

# 2. 检查 console.log
CONSOLE_COUNT=$(grep -rn "console.log" src/ --include="*.ts" 2>/dev/null | wc -l)
if [ "$CONSOLE_COUNT" -gt 0 ]; then
  echo "❌ 发现 $CONSOLE_COUNT 处 console.log"
  grep -rn "console.log" src/ --include="*.ts"
  exit 1
fi

# 3. 类型检查
pnpm exec tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ TypeScript 类型检查失败"
  exit 1
fi

# 4. Lint 检查
pnpm lint
if [ $? -ne 0 ]; then
  echo "❌ ESLint 检查失败"
  exit 1
fi

echo "✅ Code Quality Gates Passed"
```

### 交付检查清单

```
□ 已读取目标文件后再编辑
□ 无裸 any 类型（或有注释说明）
□ 无 console.log（生产代码）
□ 函数 ≤ 50 行
□ 文件 ≤ 500 行
□ useEffect 依赖完整
□ 错误处理完整（try-catch）
□ tsc --noEmit 通过
□ pnpm lint 通过
```

---

## 🔗 与其他 Skills 协作

| 阶段 | Skill |
|------|-------|
| 写代码前 | 本 Skill 检查约束 |
| 写代码中 | 知识层 Skills 提供最佳实践 |
| 写代码后 | 本 Skill 验证结果 |
| 准备提交 | `review-quality-gates` 最终审核 |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 代码示例区分 ❌ 错误 和 ✅ 正确
- [x] 检查失败有明确处理流程
- [x] 快速检查命令可直接复制使用
