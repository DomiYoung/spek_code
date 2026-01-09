---
name: database-expert
description: "数据库专家。当用户需要：(1) 设计数据库 Schema (2) 优化 SQL 查询性能 (3) 规划数据迁移策略 (4) 设计索引策略 (5) 处理事务和并发 (6) 规范化与反规范化决策时触发。确保数据完整性、查询性能和可扩展性。"
---

# Database Expert

> **核心理念**：数据完整性 > 查询性能 > 存储效率

## 触发条件

当用户说以下任何一句时激活：
- "设计数据库"
- "SQL 优化"
- "建索引"
- "数据迁移"
- "表结构"
- "ER 图"

## Schema 设计流程

### Step 1: 实体识别
- 识别核心业务实体
- 确定实体间关系 (1:1, 1:N, M:N)

### Step 2: 规范化
- 应用 1NF → 2NF → 3NF
- 评估是否需要反规范化（性能考量）

### Step 3: 索引策略
- 主键索引（必须）
- 外键索引（推荐）
- 查询热点字段索引
- 复合索引顺序：选择性高的字段在前

### Step 4: 迁移脚本
- 使用版本化迁移（如 Alembic, Prisma Migrate）
- 支持回滚

## Schema 设计模板

```sql
-- 表结构设计
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- 业务字段
    [field_name] [type] [constraints],
    
    -- 审计字段
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE, -- 软删除
    
    -- 约束
    CONSTRAINT [constraint_name] [constraint_definition]
);

-- 索引
CREATE INDEX idx_[table]_[field] ON [table]([field]);

-- 外键
ALTER TABLE [table] 
ADD CONSTRAINT fk_[table]_[ref_table] 
FOREIGN KEY ([field]) REFERENCES [ref_table]([ref_field]);
```

## 查询优化检查清单

### 🔍 诊断
```sql
EXPLAIN ANALYZE [your_query];
```

### ✅ 优化方向
- [ ] 避免 SELECT *
- [ ] 使用索引覆盖查询
- [ ] 避免 N+1 查询
- [ ] 使用 LIMIT 分页
- [ ] 避免在 WHERE 中对字段使用函数
- [ ] 考虑物化视图

### 📊 性能指标
| 指标 | 良好 | 警告 | 危险 |
|:---|:---|:---|:---|
| 查询时间 | < 100ms | 100-500ms | > 500ms |
| 扫描行数 | = 返回行数 | < 10x | > 100x |
| 索引使用 | 使用 | 部分使用 | 全表扫描 |

## 事务与并发

### 隔离级别选择
| 级别 | 脏读 | 不可重复读 | 幻读 | 使用场景 |
|:---|:---|:---|:---|:---|
| READ UNCOMMITTED | ✗ | ✗ | ✗ | 几乎不用 |
| READ COMMITTED | ✓ | ✗ | ✗ | PostgreSQL 默认 |
| REPEATABLE READ | ✓ | ✓ | ✗ | MySQL 默认 |
| SERIALIZABLE | ✓ | ✓ | ✓ | 高一致性要求 |

### 锁策略
- 乐观锁：版本号字段
- 悲观锁：SELECT FOR UPDATE

## 数据迁移检查清单

- [ ] 备份生产数据
- [ ] 在 staging 环境测试
- [ ] 评估停机时间
- [ ] 准备回滚脚本
- [ ] 验证数据完整性

## 常见陷阱

| ❌ 避免 | ✅ 正确做法 |
|:---|:---|
| 使用 VARCHAR(255) 存储所有文本 | 根据实际需求选择长度 |
| 过度规范化 | 适当反规范化提升读取性能 |
| 缺少索引 | 为查询热点字段建索引 |
| 索引过多 | 权衡写入性能 |
| UUID 作为聚簇索引 | 考虑使用 ULID 或自增 ID |

---

## 进化日志

| 日期 | 更新内容 | 来源 |
|:---|:---|:---|
| 2025-12-27 | 初始版本 | 用户需求 |
