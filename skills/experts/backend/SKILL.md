---
name: backend-expert
type: Expert
version: 1.0.0
description: |
  后端开发专家 - 基于 Python/Node.js 生产级最佳实践。
  ① 帮我干什么：API 设计、并发处理、错误处理、性能优化
  ② 什么时候出场：涉及 FastAPI、Flask、Node.js、Express、数据库、API 时自动调用
  ③ 和项目有无关系：适用于所有后端项目，是全局通用的后端专家
  关键词：API、FastAPI、Flask、Node.js、Express、Python、async、并发、事务
allowed-tools: "*"
---

# Backend Expert（后端开发专家）

> **核心理念**：安全第一，性能为本，可观测性优先。
> **来源**：[FastAPI Best Practices](https://fastapi.tiangolo.com/)、[Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)、[OWASP](https://owasp.org/)

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 代码被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **禁止 SQL 拼接** | 必须使用参数化查询 | `grep -rE "f['\"].*SELECT.*{|execute\(['\"].*\+|%s.*%\s*\(" src/` |
| **禁止明文密码** | 必须哈希存储 | `grep -rE "password\s*=\s*['\"][^'\"]+['\"]" src/` |
| **禁止堆栈暴露** | 生产环境不返回 traceback | `grep -rE "traceback\.print|exc_info=True" src/` |
| **输入验证** | 所有用户输入必须验证 | 代码审查：检查 endpoint 是否有 Pydantic/Zod |
| **错误处理** | 统一错误格式 `{ error, code, message }` | 代码审查：检查全局异常处理器 |
| **日志记录** | 关键操作有结构化日志 | `grep -rE "logger\.(info|error|warning)" src/` |
| **事务安全** | 多表操作必须使用事务 | 代码审查：检查 `@transaction` 或 `BEGIN/COMMIT` |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ Python: GIL 阻塞导致并发性能差 ⭐⭐⭐⭐⭐

**问题**: CPU 密集型任务阻塞所有请求，响应时间飙升
**检测**: `grep -rE "def (get|post|put|delete).*:$" src/ -A 10 | grep -v "await\|async"`
**修正**: 使用 `run_in_executor` 或进程池

```python
# ❌ 错误 - 阻塞整个事件循环
@app.get("/process")
async def process_data():
    result = heavy_cpu_computation()  # 阻塞！
    return result

# ✅ 正确 - 使用进程池
import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=4)

@app.get("/process")
async def process_data():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, heavy_cpu_computation)
    return result
```

### ❌ Python: async/await 混用同步阻塞 ⭐⭐⭐⭐⭐

**问题**: `async def` 内调用同步 I/O，整个事件循环卡住
**检测**: `grep -rE "async def.*:$" src/ -A 20 | grep -E "requests\.(get|post)|time\.sleep"`
**修正**: 使用异步 HTTP 客户端

```python
# ❌ 错误 - 同步 requests 阻塞事件循环
import requests

@app.get("/fetch")
async def fetch_external():
    response = requests.get("https://api.example.com")  # 阻塞！
    return response.json()

# ✅ 正确 - 使用异步 HTTP 客户端
import httpx

async_client = httpx.AsyncClient()

@app.get("/fetch")
async def fetch_external():
    response = await async_client.get("https://api.example.com")
    return response.json()
```

### ❌ Python: 资源泄漏（连接/文件未关闭）⭐⭐⭐⭐

**问题**: 数据库连接、文件句柄未关闭，资源耗尽
**检测**: `grep -rE "open\(|get_db_connection\(" src/ | grep -v "with "`
**修正**: 使用上下文管理器

```python
# ❌ 错误 - 连接可能泄漏
def get_user(user_id):
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return result.fetchone()
    # conn 永远不会关闭！

# ✅ 正确 - 使用上下文管理器
def get_user(user_id):
    with get_db_connection() as conn:
        result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result.fetchone()
    # 自动关闭连接
```

### ❌ Python: 可变默认参数陷阱 ⭐⭐⭐

**问题**: 函数调用之间共享同一个列表/字典，数据污染
**检测**: `grep -rE "def \w+\(.*=\s*\[\]|def \w+\(.*=\s*\{\}" src/`
**修正**: 使用 None 作为默认值

```python
# ❌ 错误 - 列表在调用间共享
def add_item(item, items=[]):
    items.append(item)
    return items

add_item(1)  # [1]
add_item(2)  # [1, 2] - 不是预期的 [2]！

# ✅ 正确 - 使用 None 作为默认值
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### ❌ FastAPI: Depends 生命周期误解 ⭐⭐⭐⭐⭐

**问题**: 数据库会话在请求间共享，事务污染
**检测**: `grep -rE "^db\s*=\s*SessionLocal\(\)" src/`
**修正**: 每次请求新建 session

```python
# ❌ 错误 - 全局 session 在请求间共享
db_session = SessionLocal()  # 全局！

@app.get("/users")
def get_users():
    return db_session.query(User).all()  # 事务可能污染

# ✅ 正确 - 每次请求新建 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### ❌ FastAPI: BackgroundTasks 异常吞没 ⭐⭐⭐⭐

**问题**: 后台任务失败无日志，数据丢失
**检测**: `grep -rE "background_tasks\.add_task" src/ -A 5 | grep -v "try:\|except\|logging"`
**修正**: 包装异常处理

```python
# ❌ 错误 - 异常被静默吞没
def send_email_task(email: str):
    raise Exception("SMTP connection failed")  # 无日志！

@app.post("/register")
def register(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_task, "user@example.com")
    return {"status": "ok"}

# ✅ 正确 - 包装异常处理
import logging

def send_email_task(email: str):
    try:
        # 发送邮件逻辑
        pass
    except Exception as e:
        logging.error(f"Failed to send email to {email}: {e}")
        # 可选：写入死信队列
```

### ❌ Node.js: 事件循环阻塞 ⭐⭐⭐⭐⭐

**问题**: 单个 CPU 密集任务阻塞所有请求
**检测**: `grep -rE "pbkdf2Sync|hashSync|readFileSync" src/`
**修正**: 使用异步版本或 Worker Threads

```javascript
// ❌ 错误 - 阻塞事件循环
app.get('/hash', (req, res) => {
    const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512');
    res.json({ hash });
});

// ✅ 正确 - 使用异步版本
app.get('/hash', async (req, res) => {
    const hash = await new Promise((resolve, reject) => {
        crypto.pbkdf2(password, salt, 100000, 64, 'sha512', (err, key) => {
            if (err) reject(err);
            else resolve(key);
        });
    });
    res.json({ hash });
});
```

### ❌ Node.js: 未处理的 Promise Rejection ⭐⭐⭐⭐⭐

**问题**: Promise 错误被静默吞没，应用状态异常
**检测**: `grep -rE "\.then\(" src/ | grep -v "\.catch\("`
**修正**: 全局处理或每个 Promise 都 catch

```javascript
// ❌ 错误 - 未捕获的 rejection
async function fetchData() {
    const response = await fetch(url);
    return response.json();
}

fetchData();  // 无 .catch()，错误丢失

// ✅ 正确 - 全局处理
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection:', reason);
});

// ✅ 更佳 - 每个 Promise 都处理
fetchData().catch(err => console.error(err));
```

### ❌ Node.js: 内存泄漏（缓存无限增长）⭐⭐⭐⭐

**问题**: 内存持续增长，最终 OOM
**检测**: `grep -rE "const cache = \{\}|let cache = \{\}" src/`
**修正**: 使用 LRU 缓存

```javascript
// ❌ 错误 - 全局缓存无限增长
const cache = {};
app.get('/data/:id', (req, res) => {
    cache[req.params.id] = fetchData(req.params.id);  // 无清理！
});

// ✅ 正确 - 使用 LRU 缓存
const LRU = require('lru-cache');
const cache = new LRU({ max: 500, ttl: 1000 * 60 * 5 });

app.get('/data/:id', async (req, res) => {
    const cached = cache.get(req.params.id);
    if (cached) return res.json(cached);

    const data = await fetchData(req.params.id);
    cache.set(req.params.id, data);
    res.json(data);
});
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准实现模式

### FastAPI 端点模板

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["users"])

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """创建用户 - 标准端点模板"""
    try:
        # 1. 业务逻辑验证
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "USER_EXISTS", "message": "Email already registered"}
            )

        # 2. 创建实体
        user = User(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)

        # 3. 日志记录
        logger.info(f"User created: {user.id}", extra={"user_id": user.id})

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create user: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "INTERNAL_ERROR", "message": "Failed to create user"}
        )
```

### Express.js 端点模板

```javascript
const express = require('express');
const { body, validationResult } = require('express-validator');
const logger = require('./logger');

const router = express.Router();

// 统一错误响应
const errorResponse = (res, status, error, message) => {
    return res.status(status).json({ error, message, timestamp: new Date().toISOString() });
};

// 异步错误包装器
const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

router.post('/users',
    // 输入验证
    body('email').isEmail().normalizeEmail(),
    body('name').trim().notEmpty().escape(),

    asyncHandler(async (req, res) => {
        // 验证结果检查
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return errorResponse(res, 400, 'VALIDATION_ERROR', errors.array());
        }

        const { email, name } = req.body;

        // 业务逻辑
        const existing = await User.findOne({ email });
        if (existing) {
            return errorResponse(res, 409, 'USER_EXISTS', 'Email already registered');
        }

        const user = await User.create({ email, name });

        logger.info('User created', { userId: user.id });

        res.status(201).json({
            data: { id: user.id, email: user.email, name: user.name },
            meta: { timestamp: new Date().toISOString() }
        });
    })
);

// 全局错误处理
router.use((err, req, res, next) => {
    logger.error('Unhandled error', { error: err.message, stack: err.stack });
    errorResponse(res, 500, 'INTERNAL_ERROR', 'Something went wrong');
});

module.exports = router;
```

### 生产部署配置

```bash
# FastAPI 生产配置 (Gunicorn + Uvicorn)
gunicorn app:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -

# Node.js 生产配置 (PM2)
# ecosystem.config.js
module.exports = {
    apps: [{
        name: 'api',
        script: 'dist/index.js',
        instances: 'max',
        exec_mode: 'cluster',
        max_memory_restart: '500M',
        env_production: {
            NODE_ENV: 'production',
            PORT: 3000
        }
    }]
};
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交代码前运行

### 自动审计脚本

```bash
#!/bin/bash
# backend-audit.sh

echo "🔍 Backend Expert Audit..."

# 1. SQL 注入检测
if grep -rE "f['\"].*SELECT.*{|execute\(['\"].*\+" src/; then
  echo "❌ 发现可能的 SQL 注入风险"
  exit 1
fi

# 2. 同步阻塞检测 (Python)
if grep -rE "requests\.(get|post)|time\.sleep" src/ --include="*.py" | grep -v "^#"; then
  echo "⚠️ 发现同步阻塞调用，请确认是否在 async 函数中"
fi

# 3. 同步阻塞检测 (Node.js)
if grep -rE "Sync\(" src/ --include="*.js" --include="*.ts"; then
  echo "⚠️ 发现同步 API 调用，建议使用异步版本"
fi

# 4. 资源泄漏检测
if grep -rE "open\(|get_db_connection\(" src/ | grep -v "with "; then
  echo "⚠️ 发现可能的资源泄漏，建议使用上下文管理器"
fi

# 5. 可变默认参数检测
if grep -rE "def \w+\(.*=\s*\[\]|def \w+\(.*=\s*\{\}" src/; then
  echo "⚠️ 发现可变默认参数，可能导致数据污染"
fi

# 6. 未处理的 Promise 检测
if grep -rE "\.then\(" src/ --include="*.js" --include="*.ts" | grep -v "\.catch\("; then
  echo "⚠️ 发现未处理的 Promise，建议添加 .catch()"
fi

echo "✅ Backend Audit Passed"
```

### 交付检查清单

```
□ 所有端点有输入验证（Pydantic/Zod/express-validator）
□ 统一错误响应格式 { error, code, message }
□ 敏感操作有结构化日志记录
□ 数据库操作使用事务（需要时）
□ 无 SQL 拼接（全部参数化查询）
□ 无同步阻塞调用在 async 函数中
□ 资源使用上下文管理器 / try-finally
□ 生产环境使用 WSGI/ASGI 服务器
□ 全局异常处理已配置
□ API 文档与实现一致
```

### 框架特定检查

| 框架 | 检查项 |
|------|--------|
| FastAPI | Depends 生命周期正确、BackgroundTasks 有异常处理、Pydantic 验证 |
| Flask | 应用上下文正确使用、工厂模式避免循环导入、使用 Gunicorn |
| Express | asyncHandler 包装、全局错误中间件、input 验证 |
| Node.js | 无事件循环阻塞、LRU 缓存、unhandledRejection 处理 |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 无泛泛而谈的建议（"小心"、"注意"等）
- [x] 代码块可直接复制使用
