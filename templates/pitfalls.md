# Pitfalls - 自动经验沉淀库

> **核心原则**：每次踩坑后立即记录，下次会话自动读取。实现 `踩坑 → 记录 → 学习` 闭环。

---

## 📋 快速索引

| 分类 | 条目数 | 最近更新 |
|------|--------|----------|
| 工具使用 | 0 | - |
| 代码模式 | 2 | 2025-12-29 |
| 工作流程 | 0 | - |
| 框架陷阱 | 1 | 2025-12-30 |

---

## 🔧 工具使用陷阱

<!--
格式:
### [日期] 简短标题
**现象**: 发生了什么
**根因**: 为什么发生
**修复**: 如何解决
**预防**: 下次如何避免
-->

---

## 💻 代码模式陷阱

<!-- 常见的代码编写错误和反模式 -->

### [2025-12-29] 环境变量 fallback 自引用导致 undefined

**现象**: 生产环境 API 请求返回 `405 Method Not Allowed`，请求被发送到前端服务器而非 API 服务器

**根因**: 环境变量 fallback 写成自身引用，当未设置时 fallback 依然是 `undefined`
```typescript
// ❌ 错误写法 - fallback 自引用
const BASE_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? '' : import.meta.env.VITE_API_URL);
  // ↑ 如果 VITE_API_URL 未设置，fallback 还是 undefined
```

**修复**: 为生产环境提供硬编码 fallback
```typescript
// ✅ 正确写法 - 硬编码 fallback
const BASE_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? '' : 'https://api.example.com');
```

**预防**:
- [ ] 环境变量 fallback 逻辑检查：fallback 值不能是自身
- [ ] 生产环境 API URL 必须有硬编码兜底
- [ ] 部署后验证网络请求域名是否正确

**知识价值**: ⭐⭐⭐ (逻辑隐蔽、调试耗时、跨分支差异)

### [2025-12-29] React useState 解构丢弃变量导致 ReferenceError

**现象**: 生产环境控制台报错 `ReferenceError: iframeReady is not defined`，DrawIO 编辑器弹窗无法正常显示加载状态

**根因**: useState 解构时使用 `[, setter]` 语法丢弃了状态值，但 JSX 中仍然引用该变量
```typescript
// ❌ 错误写法 - 解构时丢弃了 iframeReady
const [, setIframeReady] = useState(false);
// ...
{!iframeReady && <LoadingSpinner />}  // ← ReferenceError!
```

**修复**: 保留需要使用的状态变量
```typescript
// ✅ 正确写法 - 保留状态变量
const [iframeReady, setIframeReady] = useState(false);
```

**预防**:
- [ ] 解构 useState 时，检查是否所有被丢弃的变量确实未被使用
- [ ] 使用 ESLint 规则 `no-undef` 捕获未定义变量
- [ ] 生产构建前本地测试完整功能流程

**相关文件**: `src/components/editor/components/blocks/code/DiagramBlockWrapper.tsx`

**知识价值**: ⭐⭐⭐ (隐蔽性高、生产环境才暴露、解构语法陷阱)

---

## 📐 工作流程陷阱

<!-- 流程执行中的常见错误 -->

---

## 🏗️ 框架陷阱

<!-- 特定框架（React, Vue, ReactFlow等）的坑 -->

### [2025-12-30] SQLite 生产级约束陷阱 - 外键默认禁用

**现象**: FK 约束不生效，可以插入无效的外键值（如 `article_id=99999` 引用不存在的文章），数据完整性无法保证

**根因**: SQLite 的 `foreign_keys` 约束**默认禁用**，每次新建连接都需要手动启用
```python
# ❌ 错误写法 - 未启用外键约束
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
# FK 约束无效！可以插入无效外键

# ✅ 正确写法 - 显式启用外键约束
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")  # 🔴 关键！每次连接都要执行
```

**修复**: 在 `get_db_connection()` 函数中添加 PRAGMA 语句
```python
def get_db_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # ← 添加此行
    return conn
```

**相关陷阱**:
1. **ALTER TABLE ADD COLUMN 限制**: SQLite 不支持 `DEFAULT CURRENT_TIMESTAMP`
   ```sql
   -- ❌ 会报错: Cannot add a column with non-constant default
   ALTER TABLE raw_articles ADD COLUMN updated_at TEXT DEFAULT CURRENT_TIMESTAMP;

   -- ✅ 需要分两步
   ALTER TABLE raw_articles ADD COLUMN updated_at TEXT DEFAULT NULL;
   UPDATE raw_articles SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;
   ```

2. **列类型修改需表重建**: SQLite 不支持 `ALTER COLUMN`
   ```sql
   -- 必须使用表重建模式
   CREATE TABLE new_table (...);          -- 1. 创建新表（正确类型）
   INSERT INTO new_table SELECT ...;      -- 2. 复制数据
   DROP TABLE old_table;                  -- 3. 删除旧表
   ALTER TABLE new_table RENAME TO ...;   -- 4. 重命名
   ```

**预防**:
- [ ] 检查所有数据库连接函数是否启用 `PRAGMA foreign_keys = ON`
- [ ] SQLite 列类型修改需使用表重建模式
- [ ] `ALTER TABLE ADD COLUMN` 默认值只能是常量，不能是 `CURRENT_TIMESTAMP`
- [ ] 生产环境使用 PostgreSQL 避免这些限制

**相关文件**:
- `contentrss/backend/database.py:74` - FK 修复
- `backend/migrations/002_p0_production_fixes.sql` - 表重建示例

**知识价值**: ⭐⭐⭐⭐ (生产级隐患、跨数据库差异、难以调试、高复发性)

---

## 📝 记录模板

复制以下模板添加新条目：

```markdown
### [YYYY-MM-DD] 问题简述

**现象**: 具体发生了什么问题

**根因**: 问题的根本原因分析

**修复**: 如何解决这个问题
```代码示例（如有）```

**预防**:
- [ ] 检查项 1
- [ ] 检查项 2

**相关文件**: `path/to/file.ts`
```

---

## 🔄 自动触发规则

**何时记录**：
1. 同一问题出现 2 次
2. 调试时间 > 15 分钟
3. 需要 Web 搜索才解决的问题
4. 框架/库的非直觉行为

**会话启动时**：
1. 读取此文件
2. 根据当前任务匹配相关条目
3. 主动提醒潜在陷阱

**会话结束时**：
1. 检查是否有新发现需要记录
2. 更新相关条目的"最近验证"时间
