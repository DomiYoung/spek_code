---
name: postgresql-design
description: |
  PostgreSQL 数据库设计专家 - Schema、索引、迁移。
  Use when:
  - 设计数据库表结构
  - 规范化、外键、索引优化
  - 数据库迁移
  触发词：PostgreSQL、数据库、表设计、Schema、索引、迁移、SQL
  Related Skills: xlsx, experts/database, experts/architect
allowed-tools: Read, Grep, Bash
---

# PostgreSQL Database Design Skill

专注于 PostgreSQL 数据库设计最佳实践，包括规范化、外键约束、索引优化和迁移策略。

## 核心原则

### 1. 规范化设计
- **第一范式 (1NF)**：消除重复列，确保每列原子性
- **第二范式 (2NF)**：消除部分依赖
- **第三范式 (3NF)**：消除传递依赖
- **实用主义**：适度反规范化以提升查询性能

### 2. 主键与外键
```sql
-- ✅ 推荐：使用自增主键
id SERIAL PRIMARY KEY  -- PostgreSQL
id BIGSERIAL PRIMARY KEY  -- 大数据量

-- ✅ 推荐：外键约束 + 级联操作
category_id INT NOT NULL REFERENCES categories(id) ON DELETE SET NULL

-- ⚠️ 避免：字符串作为外键（除非是自然键如 ISO 代码）
```

### 3. 索引策略
```sql
-- 单列索引：高选择性列
CREATE INDEX idx_articles_category ON articles(category_id);

-- 复合索引：按查询频率排序
CREATE INDEX idx_articles_category_date ON articles(category_id, created_at DESC);

-- 部分索引：只索引活跃数据
CREATE INDEX idx_active_topics ON topics(status) WHERE status = 'active';
```

### 4. 命名规范
| 类型 | 规范 | 示例 |
|:--|:--|:--|
| 表名 | 复数、snake_case | `raw_articles`, `topic_evidences` |
| 主键 | `id` | `id SERIAL PRIMARY KEY` |
| 外键 | `{单数表名}_id` | `category_id`, `topic_id` |
| 索引 | `idx_{表}_{列}` | `idx_articles_category` |
| 约束 | `chk_{表}_{规则}` | `chk_articles_polarity` |

### 5. 迁移最佳实践
```sql
-- 1. 添加新列（可空，不影响现有数据）
ALTER TABLE raw_articles ADD COLUMN category_tag_id INT;

-- 2. 创建外键（不立即强制）
ALTER TABLE raw_articles 
ADD CONSTRAINT fk_raw_articles_category 
FOREIGN KEY (category_tag_id) REFERENCES tags(id)
NOT VALID;  -- 不检查现有数据

-- 3. 数据迁移
UPDATE raw_articles r 
SET category_tag_id = t.id 
FROM tags t 
WHERE r.category_key = t.tag_key;

-- 4. 验证外键
ALTER TABLE raw_articles VALIDATE CONSTRAINT fk_raw_articles_category;

-- 5.（可选）删除旧列
ALTER TABLE raw_articles DROP COLUMN category_key;
```

### 6. 查询优化
```sql
-- ✅ 推荐：使用 JOIN 获取关联数据
SELECT r.*, t.name as category_name, t.icon, t.color
FROM raw_articles r
JOIN tags t ON r.category_tag_id = t.id
WHERE t.level = 'category';

-- ⚠️ 避免：N+1 查询或多次 SELECT
```

## 常见陷阱

1. **字符串外键**：用 `category_key VARCHAR` 而非 `category_tag_id INT` — 浪费存储、无约束
2. **缺少索引**：外键列必须加索引，否则 JOIN 性能差
3. **过度规范化**：频繁 JOIN 多表反而降低性能
4. **忽略 NULL 处理**：外键允许 NULL 时要明确业务语义

## 工具推荐

- **迁移管理**：Alembic (Python)、Flyway、Liquibase
- **可视化设计**：Luna Modeler、dbdiagram.io、pgAdmin ERD
- **性能分析**：`EXPLAIN ANALYZE`、pg_stat_statements
