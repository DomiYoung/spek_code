---
name: fundamentals-network
description: |
  网络底层原理诊断 - 主动识别网络相关问题。
  Auto-trigger when:
  - 请求超时/失败 → HTTP 协议
  - 缓存不生效/过期 → 缓存策略
  - 实时通信问题 → WebSocket/SSE
  - DNS/连接慢 → 网络层
  Related Skills: fundamentals/browser, experts/backend, signalr-patterns
allowed-tools: "*"
---

# Network Fundamentals（网络底层原理）

> **Skill 类型**：Diagnostic（诊断型）
> **触发方式**：由 expert-router 根据问题症状自动加载

---

## 诊断触发矩阵

| 症状关键词 | 底层原因 | 诊断模块 |
|-----------|---------|---------|
| 请求失败、超时、504、502 | 连接/服务器问题 | HTTP Protocol |
| 缓存不更新、显示旧数据 | 缓存策略配置 | Cache Strategy |
| 接口慢、TTFB 高 | DNS/TCP/TLS | Connection |
| 实时消息延迟、断连 | WebSocket 问题 | Real-time |
| 重复请求、竞态条件 | 请求管理 | Request Management |

---

## 1. HTTP Protocol（HTTP 协议）

### 请求生命周期

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 请求生命周期                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DNS Lookup ─────────────────────────────────────────────│
│     域名 → IP 地址                                           │
│     优化: DNS 预解析 <link rel="dns-prefetch">              │
│                                                              │
│  2. TCP Connection ─────────────────────────────────────────│
│     三次握手建立连接                                          │
│     优化: Keep-Alive 复用连接, HTTP/2 多路复用               │
│                                                              │
│  3. TLS Handshake (HTTPS) ──────────────────────────────────│
│     证书验证、密钥协商                                        │
│     优化: TLS 1.3, Session Resumption                       │
│                                                              │
│  4. Request Sent ───────────────────────────────────────────│
│     发送请求头和请求体                                        │
│     优化: 压缩请求体, 减少 Cookie                            │
│                                                              │
│  5. TTFB (Time To First Byte) ──────────────────────────────│
│     等待服务器处理                                            │
│     优化: 服务端性能, CDN                                    │
│                                                              │
│  6. Content Download ───────────────────────────────────────│
│     下载响应体                                                │
│     优化: Gzip/Brotli 压缩, 分块传输                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### HTTP 状态码速查

```
1xx - 信息性响应
├── 100 Continue: 继续发送请求体
└── 101 Switching Protocols: 协议切换 (WebSocket)

2xx - 成功
├── 200 OK: 请求成功
├── 201 Created: 资源创建成功
├── 204 No Content: 成功但无响应体
└── 206 Partial Content: 范围请求成功

3xx - 重定向
├── 301 Moved Permanently: 永久重定向 (可缓存)
├── 302 Found: 临时重定向
├── 304 Not Modified: 缓存有效
└── 307/308: 保持请求方法的重定向

4xx - 客户端错误
├── 400 Bad Request: 请求格式错误
├── 401 Unauthorized: 未认证
├── 403 Forbidden: 无权限
├── 404 Not Found: 资源不存在
├── 409 Conflict: 资源冲突
├── 422 Unprocessable Entity: 验证失败
└── 429 Too Many Requests: 限流

5xx - 服务端错误
├── 500 Internal Server Error: 服务器内部错误
├── 502 Bad Gateway: 上游服务错误
├── 503 Service Unavailable: 服务不可用
└── 504 Gateway Timeout: 上游超时
```

### 常见问题诊断

**症状：请求超时**

```javascript
// ❌ 问题：无超时处理
fetch('/api/data').then(handleData);

// ✅ 修复：添加超时控制
async function fetchWithTimeout(url, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`Request timeout after ${timeout}ms`);
    }
    throw error;
  }
}

// ✅ 使用 axios 的超时
axios.get('/api/data', { timeout: 5000 });
```

---

## 2. Cache Strategy（缓存策略）

### 缓存决策流程

```
┌─────────────────────────────────────────────────────────────┐
│                     浏览器缓存决策流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  请求资源                                                    │
│      │                                                       │
│      ▼                                                       │
│  ┌─────────────────┐                                        │
│  │ 有本地缓存？     │─── No ──→ 发起网络请求                  │
│  └────────┬────────┘                                        │
│           │ Yes                                              │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │ 强缓存有效？     │─── Yes ──→ 直接使用缓存 (200 from cache)│
│  │ (Expires/       │                                        │
│  │  Cache-Control) │                                        │
│  └────────┬────────┘                                        │
│           │ No (过期)                                        │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │ 协商缓存验证     │                                        │
│  │ If-None-Match   │──→ 服务器比对                          │
│  │ If-Modified-Since│                                       │
│  └────────┬────────┘                                        │
│           │                                                  │
│     ┌─────┴─────┐                                           │
│     ▼           ▼                                           │
│  304 Not    200 OK                                          │
│  Modified   (新内容)                                         │
│  (用缓存)                                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 缓存头详解

```
强缓存（不发请求）
├── Cache-Control: max-age=31536000  # 缓存1年
├── Cache-Control: no-cache          # 必须验证
├── Cache-Control: no-store          # 禁止缓存
├── Cache-Control: private           # 仅浏览器缓存
├── Cache-Control: public            # 允许 CDN 缓存
└── Expires: Wed, 21 Oct 2025 07:28:00 GMT  # 过期时间 (旧)

协商缓存（发请求验证）
├── ETag: "33a64df551425fcc55e4d42a148795d9"  # 内容哈希
├── If-None-Match: "33a64df..."               # 客户端验证
├── Last-Modified: Wed, 21 Oct 2024 07:28:00  # 最后修改时间
└── If-Modified-Since: Wed, 21 Oct 2024...    # 客户端验证
```

### 常见问题诊断

**症状：缓存不更新**

```javascript
// ❌ 问题：静态资源使用固定 URL
<script src="/app.js"></script>

// ✅ 修复：使用内容哈希 (构建工具自动处理)
<script src="/app.a1b2c3d4.js"></script>

// ✅ API 请求禁用缓存
fetch('/api/data', {
  headers: {
    'Cache-Control': 'no-cache'
  }
});

// ✅ 强制刷新缓存
fetch('/api/data', { cache: 'no-store' });

// ✅ React Query 的缓存策略
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  staleTime: 5 * 60 * 1000,    // 5分钟内不重新请求
  gcTime: 30 * 60 * 1000,      // 30分钟后清除缓存
});
```

**症状：Service Worker 缓存过旧**

```javascript
// ✅ 更新 Service Worker 策略
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CURRENT_CACHE)
          .map((name) => caches.delete(name))
      );
    })
  );
});
```

---

## 3. Connection（连接层）

### TCP 三次握手

```
Client                                Server
   │                                     │
   │  ──── SYN (seq=x) ──────────────▶  │
   │                                     │
   │  ◀─── SYN-ACK (seq=y, ack=x+1) ──  │
   │                                     │
   │  ──── ACK (ack=y+1) ────────────▶  │
   │                                     │
   │        连接建立，开始传输            │
   │                                     │
```

### HTTP/2 多路复用

```
HTTP/1.1: 串行请求（或多连接）
┌─────────────────────────────────────┐
│ Connection 1: Request A → Response A │
│ Connection 2: Request B → Response B │
│ Connection 3: Request C → Response C │
└─────────────────────────────────────┘

HTTP/2: 单连接多路复用
┌─────────────────────────────────────┐
│ Single Connection:                   │
│   Stream 1: Request A ↔ Response A  │
│   Stream 2: Request B ↔ Response B  │
│   Stream 3: Request C ↔ Response C  │
│   (并行，无队头阻塞)                  │
└─────────────────────────────────────┘
```

### 常见问题诊断

**症状：首次请求慢（DNS/TCP/TLS）**

```html
<!-- ✅ DNS 预解析 -->
<link rel="dns-prefetch" href="//api.example.com">

<!-- ✅ 预连接（DNS + TCP + TLS） -->
<link rel="preconnect" href="https://api.example.com">

<!-- ✅ 预加载关键资源 -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
```

**症状：并发请求被阻塞**

```javascript
// ❌ HTTP/1.1 浏览器限制 6 个并发连接
// 第 7 个请求会等待

// ✅ 解决方案 1：升级到 HTTP/2
// 服务器配置，无需代码改动

// ✅ 解决方案 2：合并请求
// 将多个小请求合并为一个批量接口
const results = await fetch('/api/batch', {
  method: 'POST',
  body: JSON.stringify({ ids: [1, 2, 3, 4, 5] })
});

// ✅ 解决方案 3：使用不同域名（域名分片，仅 HTTP/1.1）
// static1.example.com, static2.example.com
```

---

## 4. Real-time Communication（实时通信）

### 方案对比

```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│     特性        │   Polling      │     SSE        │   WebSocket    │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ 方向           │ 客户端→服务器   │ 服务器→客户端   │ 双向            │
│ 连接           │ 每次新建        │ 持久 HTTP       │ 持久 TCP        │
│ 延迟           │ 高 (轮询间隔)   │ 低              │ 最低            │
│ 开销           │ 高             │ 中              │ 低              │
│ 自动重连       │ 需自己实现      │ 浏览器自动      │ 需自己实现       │
│ 适用场景       │ 兼容性要求高    │ 单向推送        │ 双向实时通信     │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

### WebSocket 生命周期

```
┌─────────────────────────────────────────────────────────────┐
│                   WebSocket 连接生命周期                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CONNECTING (0) ─────────────────────────────────────────   │
│      │                                                       │
│      │ 握手成功                                              │
│      ▼                                                       │
│  OPEN (1) ───────────────────────────────────────────────   │
│      │  ↔ 双向消息传输                                       │
│      │                                                       │
│      │ close() / 异常                                        │
│      ▼                                                       │
│  CLOSING (2) ────────────────────────────────────────────   │
│      │                                                       │
│      │ 关闭完成                                              │
│      ▼                                                       │
│  CLOSED (3) ─────────────────────────────────────────────   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 常见问题诊断

**症状：WebSocket 频繁断连**

```javascript
// ✅ 心跳保活 + 自动重连
class ReconnectingWebSocket {
  constructor(url) {
    this.url = url;
    this.reconnectDelay = 1000;
    this.maxDelay = 30000;
    this.connect();
  }
  
  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      this.reconnectDelay = 1000; // 重置延迟
      this.startHeartbeat();
    };
    
    this.ws.onclose = () => {
      this.stopHeartbeat();
      this.scheduleReconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
  
  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000); // 30秒心跳
  }
  
  stopHeartbeat() {
    clearInterval(this.heartbeatTimer);
  }
  
  scheduleReconnect() {
    setTimeout(() => {
      this.connect();
      // 指数退避
      this.reconnectDelay = Math.min(
        this.reconnectDelay * 2,
        this.maxDelay
      );
    }, this.reconnectDelay);
  }
}
```

**症状：SSE 连接中断**

```javascript
// ✅ SSE 自动重连 + 错误处理
const eventSource = new EventSource('/api/events');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleUpdate(data);
};

eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  // 浏览器会自动尝试重连
  // 可以添加 UI 提示
};

// 使用 Last-Event-ID 恢复断点
// 服务端需要支持
```

---

## 5. Request Management（请求管理）

### 竞态条件处理

```javascript
// ❌ 问题：请求竞态
let currentQuery = '';

async function search(query) {
  currentQuery = query;
  const results = await fetch(`/search?q=${query}`);
  // 如果用户快速输入，旧请求可能后返回
  setResults(await results.json()); // 可能是旧结果！
}

// ✅ 修复：AbortController
let controller = null;

async function search(query) {
  // 取消上一个请求
  if (controller) {
    controller.abort();
  }
  controller = new AbortController();
  
  try {
    const results = await fetch(`/search?q=${query}`, {
      signal: controller.signal
    });
    setResults(await results.json());
  } catch (error) {
    if (error.name !== 'AbortError') {
      throw error;
    }
  }
}

// ✅ React Query 自动处理
const { data } = useQuery({
  queryKey: ['search', query],
  queryFn: () => fetchSearch(query),
  // 自动取消过期请求
});
```

### 请求去重

```javascript
// ✅ 使用 Map 缓存进行中的请求
const pendingRequests = new Map();

async function dedupedFetch(url) {
  if (pendingRequests.has(url)) {
    return pendingRequests.get(url);
  }
  
  const promise = fetch(url).then(r => r.json());
  pendingRequests.set(url, promise);
  
  try {
    return await promise;
  } finally {
    pendingRequests.delete(url);
  }
}
```

---

## 证据采集要点
- Network 瀑布图：DNS/TCP/TLS/TTFB 阶段耗时
- 缓存响应头：Cache-Control/ETag/Last-Modified
- 可选：运行 `scripts/diagnose.sh` 采集 DNS/TLS/TTFB 初步数据

## 快速诊断清单

```markdown
## 网络问题诊断清单

### 请求失败
- [ ] 检查 Network 面板状态码
- [ ] 检查 CORS 响应头
- [ ] 检查请求是否超时
- [ ] 检查服务端日志

### 缓存问题
- [ ] 检查 Cache-Control 响应头
- [ ] 检查 ETag/Last-Modified
- [ ] 是否使用了内容哈希文件名
- [ ] Service Worker 是否过期

### 连接慢
- [ ] DNS 解析时间 (dns-prefetch)
- [ ] TCP/TLS 握手 (preconnect)
- [ ] TTFB 是否正常
- [ ] 是否启用 HTTP/2

### 实时通信
- [ ] WebSocket 是否有心跳保活
- [ ] 是否实现了自动重连
- [ ] 网络切换时是否恢复
- [ ] 消息是否有序列号防丢失
```

---

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：协议阶段、缓存语义、HTTP/2/3 与实时通信

---

**✅ 网络底层原理诊断就绪** | **主动识别通信问题**
