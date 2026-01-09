## IndexedDB 核心知识库

### 1. 架构概述
- **定位**: 浏览器端结构化数据存储，支持索引和事务
- **容量**: 通常为可用磁盘空间的 50%（Chrome）或更大
- **特点**: 异步 API、事务性、支持二进制数据

### 2. 核心概念

| 概念 | 说明 |
|------|------|
| **Database** | 数据库实例，包含多个 Object Store |
| **Object Store** | 类似表，存储 JavaScript 对象 |
| **Index** | 在字段上创建索引，加速查询 |
| **Transaction** | 所有操作必须在事务中进行 |
| **Cursor** | 遍历 Object Store 或 Index |

### 3. 常用封装库对比

| 库 | 大小 | 特点 | 适用场景 |
|---|------|------|---------|
| **idb** | ~1.2KB | Promise 封装，轻量 | 简单缓存需求 |
| **Dexie.js** | ~25KB | 完整 ORM，强类型 | 复杂数据模型 |
| **localForage** | ~8KB | 多后端支持 | 兼容性优先 |

### 4. 缓存策略模式

**TTL (Time To Live) 策略**:
```typescript
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresAt: number;  // TTL 过期时间
}

function isExpired(entry: CacheEntry<unknown>): boolean {
  return Date.now() > entry.expiresAt;
}
```

**日期感知策略** (本项目使用):
```typescript
function isCacheValid(dataDate: string): boolean {
  const today = new Date().toISOString().slice(0, 10);
  return dataDate === today;  // 数据日期 === 今天
}
```

**版本控制策略**:
```typescript
const DB_VERSION = 2;  // 升级版本号触发 onupgradeneeded
```

### 5. 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 缓存未更新 | TTL 判断错误或未清理 | 验证 isExpired 逻辑，确保 setCache 写入新数据 |
| 数据过期但仍返回 | 先返回后验证 | 改为先验证后返回，或返回同时触发后台更新 |
| 事务中断 | 事务超时或异常 | 使用 try-catch，确保事务正确关闭 |
| 版本升级失败 | onupgradeneeded 逻辑错误 | 处理所有版本迁移路径 |
| 存储满 | QuotaExceededError | 实现 LRU 清理或压缩数据 |

### 6. idb 库使用模式

```typescript
import { openDB, IDBPDatabase } from 'idb';

interface CacheDB {
  cache: {
    key: string;
    value: { data: unknown; timestamp: number; expiresAt: number };
  };
}

const dbPromise = openDB<CacheDB>('app-cache', 1, {
  upgrade(db) {
    db.createObjectStore('cache', { keyPath: 'key' });
  },
});

// 设置缓存
async function setCache(key: string, data: unknown, ttlMs: number) {
  const db = await dbPromise;
  await db.put('cache', {
    key,
    data,
    timestamp: Date.now(),
    expiresAt: Date.now() + ttlMs,
  });
}

// 获取缓存（带过期检查）
async function getCache<T>(key: string): Promise<T | null> {
  const db = await dbPromise;
  const entry = await db.get('cache', key);
  if (!entry || Date.now() > entry.expiresAt) {
    return null;  // 过期或不存在
  }
  return entry.data as T;
}

// 清除所有缓存
async function clearAllCache() {
  const db = await dbPromise;
  await db.clear('cache');
}
```

### 7. 调试技巧

**Chrome DevTools**:
- Application → IndexedDB 查看数据库内容
- 右键删除数据库或条目

**日志追踪**:
```typescript
console.log(`🔍 缓存检查: ${key} (数据日期: ${dataDate} vs 今天: ${today})`);
console.log(`✅ 缓存命中: ${key}`);
console.log(`❌ 缓存过期: ${key}`);
console.log(`📦 已缓存: ${key}`);
```

### 8. 最佳实践

- ✅ 使用 `idb` 或 `Dexie.js` 封装原生 API
- ✅ 为缓存条目设置明确的过期策略
- ✅ 提供手动刷新机制让用户强制更新
- ✅ 使用 try-catch 处理所有 IndexedDB 操作
- ✅ 在 Service Worker 中结合使用实现离线优先
- ❌ 不要存储敏感数据（无加密）
- ❌ 不要假设存储永远可用（可能被清理）
```
