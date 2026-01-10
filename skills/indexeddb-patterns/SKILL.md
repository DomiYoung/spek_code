---
name: indexeddb-patterns
description: |
  IndexedDB/Dexie 缓存最佳实践。当涉及本地存储、缓存策略、离线数据、
  Dexie 操作时自动触发。
  关键词：IndexedDB、Dexie、缓存、本地存储、离线、SWR、stale-while-revalidate。
  【性能关键】包含批量操作、事务管理、缓存失效策略。
allowed-tools: Read, Grep, Glob
---

# IndexedDB / Dexie 缓存最佳实践

## 项目架构

```
src/features/workflow-editor/utils/
└── workflowCache.ts        # Dexie 缓存实现

技术栈：
- Dexie 4.x（IndexedDB 封装）
- SWR 模式（Stale-While-Revalidate）
```

---

## 1. 硬性约束 (Hard Constraints)

### 操作约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 批量操作必须使用 bulkPut/bulkAdd | 禁止循环中单条 put | `grep -rn "for.*await.*\.put(" src/ --include="*.ts"` | 🔴 Critical |
| 读写事务必须用 'rw' 模式 | 读事务中禁止写入 | `grep -A5 "transaction('r'" src/ --include="*.ts" \| grep "\.put\|\.add\|\.delete"` | 🔴 Critical |
| 异步操作必须 await | 禁止 fire-and-forget | `grep -rn "db\.[a-z]*\.(put\|add\|delete)(" src/ --include="*.ts" \| grep -v "await"` | 🔴 Critical |
| 索引字段类型必须一致 | 存取时类型相同 | 手动检查 put/get 调用 | 🟡 Warning |

### 缓存约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 必须有过期策略 | TTL 或版本控制 | `grep -rn "updatedAt\|expiresAt\|version" src/ --include="*.ts"` | 🟡 Warning |
| 必须处理 QuotaExceededError | 存储空间不足处理 | `grep -rn "QuotaExceededError" src/ --include="*.ts"` | 🔴 Critical |
| 后台刷新必须有错误处理 | 不能静默失败 | `grep -A10 "refreshInBackground\|Background" src/ --include="*.ts" \| grep "catch\|try"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 循环中单条写入

**问题**：每条数据单独 put，导致 N 次事务开销，性能极差。

**检测**：
```bash
# 检测循环中的 put 操作
grep -rn "for.*{" src/ --include="*.ts" -A10 | \
  grep -B5 "await.*\.put("

# 检测 forEach 中的 put
grep -rn "\.forEach.*async" src/ --include="*.ts" -A5 | \
  grep "\.put\|\.add"
```

**修正**：
```typescript
// ❌ 错误：N 次事务（慢）
for (const item of items) {
  await db.workflows.put(item);  // 每次都开事务
}

// ✅ 正确：1 次事务（快）
await db.workflows.bulkPut(items);

// ✅ 正确：批量删除
await db.workflows.bulkDelete(ids);

// ✅ 正确：批量添加
await db.workflows.bulkAdd(items);
```

---

### 反模式 2.2: 读事务中写入

**问题**：在只读事务中执行写操作，可能导致死锁或数据不一致。

**检测**：
```bash
# 检测 'r' 事务中是否有写操作
grep -A10 "transaction('r'" src/ -r --include="*.ts" | \
  grep "\.put\|\.add\|\.delete\|\.update"
```

**修正**：
```typescript
// ❌ 错误：读事务中写入
await db.transaction('r', db.workflows, async () => {
  const data = await db.workflows.get(id);
  await db.workflows.put(modified);  // 💥 读事务中写入！
});

// ✅ 正确：使用 'rw' 事务
await db.transaction('rw', db.workflows, async () => {
  const data = await db.workflows.get(id);
  await db.workflows.put(modified);  // ✅ 读写事务
});
```

---

### 反模式 2.3: 忘记 await 异步操作

**问题**：IndexedDB 操作是异步的，忘记 await 会导致数据未保存就继续执行。

**检测**：
```bash
# 检测没有 await 的数据库操作
grep -rn "db\.[a-z]*\.(put\|add\|delete\|update\|clear)(" src/ --include="*.ts" | \
  grep -v "await\|return"
```

**修正**：
```typescript
// ❌ 错误：fire-and-forget
db.workflows.put(data);
console.log('已保存');  // 实际可能还没保存！

// ✅ 正确：等待完成
await db.workflows.put(data);
console.log('已保存');  // 确保已保存
```

---

### 反模式 2.4: 索引字段类型不一致

**问题**：存入和读取时 ID 类型不同，导致查询失败。

**检测**：
```bash
# 检测 put 和 get 中 id 类型是否一致
grep -rn "\.put({.*id:" src/ --include="*.ts"
grep -rn "\.get(" src/ --include="*.ts"
# 手动比对类型
```

**修正**：
```typescript
// ❌ 错误：类型不一致
await db.workflows.put({ id: 123, ... });     // number
await db.workflows.get('123');                 // string - 找不到！

// ✅ 正确：类型统一
await db.workflows.put({ id: '123', ... });   // string
await db.workflows.get('123');                 // string - 匹配
```

---

### 反模式 2.5: 全表扫描查询

**问题**：不使用索引，对大表进行 filter 操作，O(n) 复杂度。

**检测**：
```bash
# 检测 toArray() 后的 filter
grep -rn "\.toArray()" src/ --include="*.ts" -A3 | \
  grep "\.filter("
```

**修正**：
```typescript
// ❌ 错误：全表扫描（慢）
const all = await db.workflows.toArray();
const drafts = all.filter(w => w.isDraft);  // O(n)

// ✅ 正确：使用索引查询（快）
const drafts = await db.workflows
  .where('isDraft')
  .equals(true)
  .toArray();  // O(log n)
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 Dexie 数据库设置

```typescript
import Dexie, { Table } from 'dexie';

interface WorkflowCache {
  id: string;
  data: BackendWorkflowData;
  updatedAt: number;
  isDraft: boolean;
}

class WorkflowDatabase extends Dexie {
  workflows!: Table<WorkflowCache>;

  constructor() {
    super('WorkflowDB');
    this.version(1).stores({
      workflows: 'id, updatedAt, isDraft'  // 索引定义
    });
  }
}

export const db = new WorkflowDatabase();
```

### 3.2 SWR 缓存模式

```typescript
/**
 * Stale-While-Revalidate 模式
 * 1. 先返回缓存数据（stale）
 * 2. 后台请求新数据
 * 3. 更新缓存和 UI
 */

async function getWorkflowWithSWR(id: string): Promise<WorkflowData> {
  // 1. 先尝试读取缓存
  const cached = await db.workflows.get(id);

  if (cached) {
    // 2. 立即返回缓存数据
    // 3. 后台刷新（不阻塞）
    refreshInBackground(id);
    return cached.data;
  }

  // 4. 无缓存，必须等待网络请求
  return await fetchAndCache(id);
}

async function refreshInBackground(id: string) {
  try {
    const freshData = await api.getWorkflow(id);
    await db.workflows.put({
      id,
      data: freshData,
      updatedAt: Date.now(),
      isDraft: false,
    });
    // 通知 UI 更新
    notifyUpdate(id);
  } catch (error) {
    // 后台刷新失败要记录，不能静默
    console.warn('Background refresh failed:', error);
  }
}
```

### 3.3 事务管理

```typescript
// 使用事务保证一致性
await db.transaction('rw', db.workflows, async () => {
  // 所有操作在同一事务中
  await db.workflows.delete(oldId);
  await db.workflows.add(newData);
  await db.workflows.update(relatedId, { updated: true });
});
// 事务失败会自动回滚
```

### 3.4 缓存失效策略

```typescript
const CACHE_TTL = 5 * 60 * 1000;  // 5 分钟

// 1. 时间过期
async function getWithExpiry(id: string) {
  const cached = await db.workflows.get(id);

  if (cached && Date.now() - cached.updatedAt < CACHE_TTL) {
    return cached.data;  // 缓存有效
  }

  return await fetchAndCache(id);  // 缓存过期
}

// 2. 条件清理（定时任务）
async function cleanupOldCache() {
  const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  await db.workflows
    .where('updatedAt')
    .below(oneWeekAgo)
    .delete();
}
```

### 3.5 与 React Query 集成

```typescript
import { useQuery, useQueryClient } from '@tanstack/react-query';

function useWorkflow(id: string) {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: ['workflow', id],
    queryFn: async () => {
      // 先检查 IndexedDB 缓存
      const cached = await db.workflows.get(id);
      if (cached) {
        // 后台刷新
        fetchAndCache(id).then(() => {
          queryClient.invalidateQueries(['workflow', id]);
        });
        return cached.data;
      }
      return await fetchAndCache(id);
    },
    staleTime: 5 * 60 * 1000,  // 5 分钟内不重新请求
  });
}
```

### 3.6 错误处理

```typescript
async function safePut(data: WorkflowCache) {
  try {
    await db.workflows.put(data);
  } catch (error) {
    if (error.name === 'QuotaExceededError') {
      // 存储空间不足，清理旧缓存后重试
      await cleanupOldCache();
      await db.workflows.put(data);
    } else if (error.name === 'ConstraintError') {
      // 主键冲突，改用 update
      await db.workflows.update(data.id, data);
    } else {
      throw error;
    }
  }
}
```

---

## 4. 自我验证 (Self-Verification)

### IndexedDB 合规审计脚本

```bash
#!/bin/bash
# indexeddb-audit.sh - IndexedDB/Dexie 代码合规检查

echo "💾 IndexedDB 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测循环中单条写入
echo -e "\n📦 检测批量操作..."
LOOP_PUT=$(grep -rn "for.*{" src/ --include="*.ts" -A10 2>/dev/null | \
  grep -c "await.*\.put(" || echo "0")

if [ "$LOOP_PUT" -gt 0 ]; then
    echo "❌ 发现循环中的 put 操作（应使用 bulkPut）"
    grep -rn "for.*{" src/ --include="*.ts" -A10 2>/dev/null | \
      grep -B5 "await.*\.put(" | head -10
    ((ERRORS++))
else
    echo "✅ 批量操作使用正常"
fi

# 2. 检测读事务中写入
echo -e "\n🔒 检测事务模式..."
RW_VIOLATION=$(grep -A10 "transaction('r'" src/ -r --include="*.ts" 2>/dev/null | \
  grep -c "\.put\|\.add\|\.delete" || echo "0")

if [ "$RW_VIOLATION" -gt 0 ]; then
    echo "❌ 读事务中有写操作（应使用 'rw' 模式）"
    grep -A10 "transaction('r'" src/ -r --include="*.ts" 2>/dev/null | \
      grep -B5 "\.put\|\.add\|\.delete" | head -10
    ((ERRORS++))
else
    echo "✅ 事务模式正确"
fi

# 3. 检测未 await 的操作
echo -e "\n⏳ 检测异步等待..."
NO_AWAIT=$(grep -rn "db\.[a-z]*\.(put\|add\|delete\|update\|clear)(" src/ --include="*.ts" 2>/dev/null | \
  grep -v "await\|return" | wc -l | tr -d ' ')

if [ "$NO_AWAIT" -gt 0 ]; then
    echo "❌ 发现未 await 的数据库操作:"
    grep -rn "db\.[a-z]*\.(put\|add\|delete\|update\|clear)(" src/ --include="*.ts" 2>/dev/null | \
      grep -v "await\|return" | head -5
    ((ERRORS++))
else
    echo "✅ 异步操作正确等待"
fi

# 4. 检测 QuotaExceededError 处理
echo -e "\n💽 检测存储错误处理..."
QUOTA_HANDLER=$(grep -rn "QuotaExceededError" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$QUOTA_HANDLER" -eq 0 ]; then
    echo "⚠️ 未发现 QuotaExceededError 处理"
else
    echo "✅ 已配置存储空间错误处理 ($QUOTA_HANDLER 处)"
fi

# 5. 检测全表扫描
echo -e "\n🔍 检测查询优化..."
FULL_SCAN=$(grep -rn "\.toArray()" src/ --include="*.ts" -A3 2>/dev/null | \
  grep -c "\.filter(" || echo "0")

if [ "$FULL_SCAN" -gt 0 ]; then
    echo "⚠️ 发现 toArray().filter() 模式（建议使用 where 查询）"
else
    echo "✅ 查询优化正常"
fi

# 6. 检测缓存过期策略
echo -e "\n⏰ 检测缓存过期..."
EXPIRY=$(grep -rn "updatedAt\|expiresAt\|CACHE_TTL" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$EXPIRY" -eq 0 ]; then
    echo "⚠️ 未发现缓存过期策略"
else
    echo "✅ 已配置缓存过期策略"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ IndexedDB 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 批量操作使用 `bulkPut/bulkAdd/bulkDelete`
- [ ] 读写操作使用 `'rw'` 事务模式
- [ ] 所有数据库操作都有 `await`
- [ ] 索引字段类型一致（存取匹配）
- [ ] 使用 `where()` 代替 `filter()`
- [ ] 配置了缓存过期策略（TTL）
- [ ] 处理了 `QuotaExceededError`
- [ ] 后台刷新有错误处理

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `reactflow-patterns` | 节点数据持久化到 workflowCache |
| `react-query-patterns` | 双层缓存策略（内存 + IndexedDB） |
| `zustand-patterns` | 状态初始化时从缓存恢复 |
| `code-quality-gates` | 检查事务使用、异步等待 |

### 关联文件

- `src/features/workflow-editor/utils/workflowCache.ts`
- `src/utils/db/*.ts`

---

**✅ IndexedDB Patterns v2.0.0** | **标准 4 Section 已集成**
