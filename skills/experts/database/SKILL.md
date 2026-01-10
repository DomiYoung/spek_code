---
name: database-expert
description: |
  数据库专家。当涉及 Schema 设计、索引优化、迁移脚本、SQL 查询时自动触发。
  关键词：数据库、表设计、索引、SQL、迁移、PostgreSQL、SQLite、外键。
  【生产级标准】确保数据完整性和查询性能。
allowed-tools: Read, Grep, Bash
---

# 数据库专家 (Database Expert)

> **核心理念**：数据是系统的基石，任何 Schema 缺陷都会成为技术债务。
> **适用范围**：表设计、索引优化、迁移脚本、SQL 查询、性能调优。

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **主键设计** | 必须有主键，推荐 UUID/Snowflake | `CREATE TABLE` 必须包含 `PRIMARY KEY` |
| **外键约束** | 关联字段必须定义外键约束 | `_id` 结尾字段必须有 `REFERENCES` |
| **审计字段** | 必须包含 `created_at`, `updated_at` | 表必须包含时间戳字段 |
| **索引覆盖** | WHERE/JOIN/ORDER BY 字段必须有索引 | EXPLAIN ANALYZE 验证 |
| **非空约束** | 核心业务字段必须 `NOT NULL` | `NOT NULL` 占比应 > 50% |

### 审计命令

```bash
# 检查是否缺少主键
grep -L "PRIMARY KEY" schema/*.sql

# 检查是否缺少外键
grep -E "_id\s+(INTEGER|BIGINT|UUID)" schema/*.sql | grep -v "REFERENCES"

# 检查是否缺少审计字段
grep -L "created_at" schema/*.sql
```

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 隐式外键 (Trust Me FK) ⭐⭐⭐⭐⭐

**问题**: 外键字段没有约束，完全靠应用层自觉
**检测**: `grep -E "_id\s+(INTEGER|BIGINT)" schema/*.sql | grep -v "REFERENCES"`
**修正**: 添加外键约束

```sql
-- ❌ 禁止
CREATE TABLE orders (
  user_id INTEGER,  -- 没有约束
  ...
);

-- ✅ 正确
CREATE TABLE orders (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  ...
);
```

### ❌ NULL 地狱 (Default Missing) ⭐⭐⭐⭐⭐

**问题**: 状态和数值字段默认为 NULL，导致 NullPointer
**检测**: `grep -E "(status|points|count)\s+\w+" schema/*.sql | grep -v "DEFAULT"`
**修正**: 添加 DEFAULT 值和 NOT NULL 约束

```sql
-- ❌ 禁止
CREATE TABLE users (
  status VARCHAR(20),  -- 默认为 NULL
  points INTEGER       -- 默认为 NULL
);

-- ✅ 正确
CREATE TABLE users (
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  points INTEGER NOT NULL DEFAULT 0
);
```

### ❌ 低基数索引 (Useless Index) ⭐⭐⭐⭐

**问题**: 在枚举极少的字段建索引，无效且拖慢写入
**检测**: 检查 gender、status、is_active 等字段的索引
**修正**: 删除低基数索引，改用复合索引

```sql
-- ❌ 禁止 - 基数过低
CREATE INDEX idx_users_gender ON users(gender);

-- ✅ 正确 - 复合索引
CREATE INDEX idx_users_status_created ON users(status, created_at);
```

### ❌ SELECT * 查询 ⭐⭐⭐

**问题**: 返回不必要字段，浪费带宽和内存
**检测**: `grep -rn "SELECT \*" src/ --include="*.ts"`
**修正**: 显式列出需要的字段

```sql
-- ❌ 禁止
SELECT * FROM users WHERE id = 1;

-- ✅ 正确
SELECT id, name, email FROM users WHERE id = 1;
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### 标准表结构模板

```sql
CREATE TABLE example (
  -- 主键
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- 业务字段
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',

  -- 外键
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- 审计字段
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_example_user_id ON example(user_id);
CREATE INDEX idx_example_status_created ON example(status, created_at);
```

### 索引设计原则

| 场景 | 索引类型 | 示例 |
|------|---------|------|
| 外键字段 | 单列索引 | `CREATE INDEX idx_orders_user_id ON orders(user_id)` |
| 范围查询 | 复合索引 | `CREATE INDEX idx_orders_date ON orders(created_at DESC)` |
| 等值+范围 | 复合索引 | `CREATE INDEX idx_status_date ON orders(status, created_at)` |

### 迁移脚本规范

```sql
-- migrations/001_create_users.up.sql
BEGIN;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMIT;

-- migrations/001_create_users.down.sql
BEGIN;
DROP TABLE IF EXISTS users;
COMMIT;
```

### 数据库特定配置

| 数据库 | 强制配置 |
|--------|---------|
| **SQLite** | `PRAGMA foreign_keys = ON;` |
| **PostgreSQL** | 使用 pgbouncer 连接池 |

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交 Schema 前必须运行

### Schema 完整性检查

```bash
#!/bin/bash
# schema-audit.sh

echo "🔍 Database Schema Audit..."

# 1. 检查主键
MISSING_PK=$(grep -L "PRIMARY KEY" schema/*.sql 2>/dev/null | wc -l)
if [ "$MISSING_PK" -gt 0 ]; then
  echo "❌ 发现 $MISSING_PK 个表缺少主键"
  grep -L "PRIMARY KEY" schema/*.sql
  exit 1
fi

# 2. 检查外键
FK_ISSUES=$(grep -E "_id\s+(INTEGER|BIGINT|UUID)" schema/*.sql | grep -v "REFERENCES" | wc -l)
if [ "$FK_ISSUES" -gt 0 ]; then
  echo "❌ 发现 $FK_ISSUES 处隐式外键"
  grep -E "_id\s+(INTEGER|BIGINT|UUID)" schema/*.sql | grep -v "REFERENCES"
  exit 1
fi

# 3. 检查审计字段
MISSING_AUDIT=$(grep -L "created_at" schema/*.sql 2>/dev/null | wc -l)
if [ "$MISSING_AUDIT" -gt 0 ]; then
  echo "❌ 发现 $MISSING_AUDIT 个表缺少审计字段"
  grep -L "created_at" schema/*.sql
  exit 1
fi

echo "✅ Schema Audit Passed"
```

### 索引健康度检查 (PostgreSQL)

```sql
-- 检查无索引的外键
SELECT
    conrelid::regclass AS table_name,
    conname AS foreign_key,
    pg_get_constraintdef(oid) AS constraint_def
FROM pg_constraint
WHERE contype = 'f'
AND NOT EXISTS (
    SELECT 1 FROM pg_index
    WHERE indrelid = conrelid
    AND indkey::int[] @> conkey::int[]
);
-- ❌ 如果返回结果不为空，需要添加索引
```

### 交付检查清单

```
□ 所有表有主键
□ 所有 _id 字段有外键约束
□ 所有表有 created_at/updated_at
□ 核心字段有 NOT NULL 约束
□ 外键字段有索引
□ 无 SELECT * 查询
□ 迁移脚本有 up/down 对称
□ SQLite 启用 foreign_keys
```

---

## 🔗 与其他 Skills 协作

| 阶段 | Skill |
|------|-------|
| Schema 设计 | 本 Skill 提供约束 |
| 代码实现 | `backend-expert` 配合 |
| 质量审计 | `quality-expert` 验收 |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含 **检测** 逻辑和修正方案
- [x] 代码示例区分 ❌ 错误 和 ✅ 正确
- [x] 自我验证包含可执行脚本
- [x] 快速检查命令可直接复制使用
