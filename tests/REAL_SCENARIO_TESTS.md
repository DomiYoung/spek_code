# 真实场景测试用例 (Real Scenario Test Cases)

> **目的**：验证 Skills 在实际编码场景中是否有效触发并提供正确指导
> **方法**：模拟开发者常见错误，执行 Skill 的审计规则，检查是否能捕获

---

## 测试用例总览

| ID | Skill | 场景 | 预期结果 |
|----|-------|------|---------|
| TC-001 | code-quality-gates | 裸 any 类型 | 检测到并警告 |
| TC-002 | code-quality-gates | console.log 残留 | 检测到并拒绝 |
| TC-003 | zustand-patterns | 缺少 selector | 警告性能问题 |
| TC-004 | react-query-patterns | 缺少 staleTime | 建议配置 |
| TC-005 | review-quality-gates | 巨型提交 | 拒绝并要求拆分 |

---

## TC-001: 裸 any 类型检测

### Skill
`code-quality-gates`

### 场景描述
开发者写了一个工具函数，使用了未注释的 `any` 类型。

### 违规代码
```typescript
// test-bad-code/any-violation.ts
export function processData(data: any) {
  const items: any[] = data.items;
  return items.map((item: any) => item.value);
}
```

### 审计命令
```bash
grep -rn ": any" test-bad-code/ --include="*.ts"
```

### 预期输出
```
test-bad-code/any-violation.ts:2:... data: any ...
test-bad-code/any-violation.ts:3:... any[] ...
test-bad-code/any-violation.ts:4:... item: any ...
```

### 通过标准
- ✅ 命令输出检测到 3 处 `any`
- ✅ Skill 提供修正建议（添加具体类型或注释）

### 修正后代码
```typescript
// 正确写法
interface DataItem {
  value: string;
}

interface InputData {
  items: DataItem[];
}

export function processData(data: InputData): string[] {
  return data.items.map((item) => item.value);
}
```

---

## TC-002: console.log 残留检测

### Skill
`code-quality-gates`

### 场景描述
开发者调试完成后忘记删除 console.log。

### 违规代码
```typescript
// test-bad-code/console-violation.ts
export function calculateTotal(items: number[]): number {
  console.log('items:', items);  // 调试代码残留
  const total = items.reduce((a, b) => a + b, 0);
  console.log('total:', total);  // 调试代码残留
  return total;
}
```

### 审计命令
```bash
grep -rn "console.log" test-bad-code/ --include="*.ts"
```

### 预期输出
```
test-bad-code/console-violation.ts:3:  console.log('items:', items);
test-bad-code/console-violation.ts:5:  console.log('total:', total);
```

### 通过标准
- ✅ 命令检测到 2 处 console.log
- ✅ Skill 明确拒绝提交
- ✅ 提供修正建议（删除或使用 logger）

### 修正后代码
```typescript
export function calculateTotal(items: number[]): number {
  return items.reduce((a, b) => a + b, 0);
}
```

---

## TC-003: Zustand 缺少 Selector

### Skill
`zustand-patterns`

### 场景描述
开发者直接使用整个 store 状态，导致不必要的重渲染。

### 违规代码
```typescript
// test-bad-code/zustand-violation.tsx
import { useStore } from '../stores/appStore';

function UserProfile() {
  // ❌ 获取整个 store，任何状态变化都会触发重渲染
  const store = useStore();

  return <div>{store.user.name}</div>;
}
```

### 检测方法
代码审查：检查是否使用 `useStore()` 无参数形式

### 预期结果
Skill 应警告：
- 使用选择器 `useStore((state) => state.user.name)` 避免不必要渲染
- 配合 `shallow` 比较优化

### 修正后代码
```typescript
import { useStore } from '../stores/appStore';

function UserProfile() {
  // ✅ 只订阅需要的状态
  const userName = useStore((state) => state.user.name);

  return <div>{userName}</div>;
}
```

---

## TC-004: React Query 缺少 staleTime

### Skill
`react-query-patterns`

### 场景描述
开发者使用 useQuery 但未配置 staleTime，导致频繁请求。

### 违规代码
```typescript
// test-bad-code/react-query-violation.tsx
import { useQuery } from '@tanstack/react-query';

function UserList() {
  // ❌ 没有 staleTime，每次 mount 都会请求
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  return <div>{data?.map(u => u.name)}</div>;
}
```

### 检测方法
代码审查：检查 useQuery 配置是否包含 staleTime

### 预期结果
Skill 应建议：
- 添加合理的 `staleTime`（如 5 分钟）
- 考虑是否需要 `gcTime`

### 修正后代码
```typescript
import { useQuery } from '@tanstack/react-query';

function UserList() {
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000,  // 5 分钟内不重新请求
    gcTime: 10 * 60 * 1000,    // 10 分钟后清理缓存
  });

  return <div>{data?.map(u => u.name)}</div>;
}
```

---

## TC-005: 巨型提交检测

### Skill
`review-quality-gates`

### 场景描述
开发者一次性提交 800 行变更，包含多个不相关功能。

### 模拟场景
```bash
# 模拟大量变更
git diff --stat
# 输出:
# 15 files changed, 650 insertions(+), 150 deletions(-)
```

### 审计命令
```bash
LINES=$(git diff --stat | tail -1 | grep -oE '[0-9]+' | head -1)
if [ "$LINES" -gt 500 ]; then
  echo "❌ 变更超过 500 行，必须拆分"
fi
```

### 预期结果
- ✅ 检测到变更超过 500 行
- ✅ 拒绝提交
- ✅ 建议拆分为多个小提交

---

## 执行方法

### 方式一：手动执行
1. 创建 `test-bad-code/` 目录
2. 写入违规代码文件
3. 执行审计命令
4. 验证输出符合预期

### 方式二：自动化脚本
```bash
#!/bin/bash
# run-real-tests.sh

echo "═══════════════════════════════════════════════════════════"
echo "🧪 Real Scenario Tests for Skills"
echo "═══════════════════════════════════════════════════════════"

# 创建测试目录
mkdir -p test-bad-code

# TC-001: any 类型测试
cat > test-bad-code/any-violation.ts << 'EOF'
export function processData(data: any) {
  const items: any[] = data.items;
  return items.map((item: any) => item.value);
}
EOF

echo ""
echo "TC-001: 裸 any 类型检测"
echo "─────────────────────────────────────────────────────────"
ANY_COUNT=$(grep -rn ": any" test-bad-code/ --include="*.ts" | wc -l | tr -d ' ')
if [ "$ANY_COUNT" -gt 0 ]; then
  echo "✅ PASS - 检测到 $ANY_COUNT 处 any 类型"
  grep -rn ": any" test-bad-code/ --include="*.ts"
else
  echo "❌ FAIL - 未检测到 any 类型"
fi

# TC-002: console.log 测试
cat > test-bad-code/console-violation.ts << 'EOF'
export function calculateTotal(items: number[]): number {
  console.log('items:', items);
  const total = items.reduce((a, b) => a + b, 0);
  console.log('total:', total);
  return total;
}
EOF

echo ""
echo "TC-002: console.log 残留检测"
echo "─────────────────────────────────────────────────────────"
CONSOLE_COUNT=$(grep -rn "console.log" test-bad-code/ --include="*.ts" | wc -l | tr -d ' ')
if [ "$CONSOLE_COUNT" -gt 0 ]; then
  echo "✅ PASS - 检测到 $CONSOLE_COUNT 处 console.log"
  grep -rn "console.log" test-bad-code/ --include="*.ts"
else
  echo "❌ FAIL - 未检测到 console.log"
fi

# 清理
rm -rf test-bad-code

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "测试完成"
echo "═══════════════════════════════════════════════════════════"
```

---

## 验收标准

| 测试 | 通过条件 |
|------|---------|
| TC-001 | grep 检测到 ≥3 处 any |
| TC-002 | grep 检测到 ≥2 处 console.log |
| TC-003 | 代码审查发现 useStore() 无参数调用 |
| TC-004 | 代码审查发现 useQuery 缺少 staleTime |
| TC-005 | 变更行数检查脚本正确拒绝 >500 行提交 |

---

**Created**: 2026-01-09
**Purpose**: 验证 Skills 实际有效性
