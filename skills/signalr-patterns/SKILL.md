---
name: signalr-patterns
description: |
  SignalR 8.x 实时通信专家 - WebSocket、消息推送。
  Use when:
  - 实现实时通信、WebSocket
  - 断线重连、消息可靠性
  - Hub 连接管理
  触发词：SignalR、WebSocket、实时、消息推送、断线重连、Hub
  Related Skills: react-query-patterns, zustand-patterns, oidc-auth-patterns
allowed-tools: Read, Grep, Glob
---

# SignalR 8.x 实时通信

## 项目架构

```
src/features/moss-chat-signalr/
├── index.ts                    # 主入口
├── types/
│   └── index.ts                # 类型定义
├── hooks/
│   └── useStreamingText.ts     # 流式文本 Hook
└── components/
    └── ...
```

---

## 1. 硬性约束 (Hard Constraints)

### 连接管理约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 事件监听必须清理 | `connection.on` 必须有对应 `connection.off` | `grep -rn "connection\.on(" --include="*.tsx" \| wc -l` vs `grep -rn "connection\.off(" --include="*.tsx" \| wc -l` | 🔴 Critical |
| 发送前必须检查状态 | `invoke` 前必须检查 `connection.state` | `grep -B5 "\.invoke(" src/ --include="*.ts" \| grep -v "connection.state"` | 🔴 Critical |
| Token 必须动态获取 | `accessTokenFactory` 必须是函数 | `grep -A3 "accessTokenFactory" src/ --include="*.ts"` | 🟡 Warning |
| 必须处理断线 | 必须有 `onclose` 处理器 | `grep -rn "\.onclose(" src/ --include="*.ts"` | 🔴 Critical |

### 消息处理约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 消息必须有 ID | 每条消息必须有唯一标识 | 手动检查消息类型定义 | 🟡 Warning |
| 流式消息必须标记完成 | `StreamingMessage` 必须有对应 `MessageComplete` | `grep -c "StreamingMessage\|MessageComplete" src/` | 🟡 Warning |
| 重试必须有上限 | 重试次数 ≤ 5 | `grep -rn "retries\|retry" src/ --include="*.ts"` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 未清理事件监听

**问题**：组件卸载后 SignalR 事件监听器仍然存在，导致内存泄漏和重复回调。

**检测**：
```bash
# 检测 useEffect 中有 connection.on 但无 connection.off
grep -A20 "useEffect" src/ -r --include="*.tsx" | \
  grep -B10 "connection\.on" | \
  grep -L "connection\.off"

# 统计 on/off 数量是否匹配
echo "on 调用: $(grep -rn 'connection\.on(' src/ --include='*.tsx' | wc -l)"
echo "off 调用: $(grep -rn 'connection\.off(' src/ --include='*.tsx' | wc -l)"
```

**修正**：
```typescript
// ❌ 错误：组件卸载后仍在监听
useEffect(() => {
  connection.on('ReceiveMessage', handleMessage);
}, []);

// ✅ 正确：清理监听
useEffect(() => {
  const handler = (msg: Message) => handleMessage(msg);
  connection.on('ReceiveMessage', handler);

  return () => {
    connection.off('ReceiveMessage', handler);  // 必须清理
  };
}, []);
```

---

### 反模式 2.2: 未检查连接状态

**问题**：调用 `invoke` 时连接可能未就绪，导致运行时错误。

**检测**：
```bash
# 检测 invoke 前是否有状态检查
grep -B5 "\.invoke(" src/ -r --include="*.ts" | \
  grep -v "connection\.state\|HubConnectionState" | \
  grep "invoke"
```

**修正**：
```typescript
// ❌ 错误：连接可能未就绪
async function send(message: string) {
  await connection.invoke('SendMessage', message);
}

// ✅ 正确：检查连接状态
async function send(message: string) {
  if (connection.state !== signalR.HubConnectionState.Connected) {
    throw new Error('SignalR not connected');
  }
  await connection.invoke('SendMessage', message);
}
```

---

### 反模式 2.3: Token 硬编码

**问题**：Token 在连接时硬编码，过期后无法自动刷新。

**检测**：
```bash
# 检测 accessTokenFactory 是否返回静态值
grep -A5 "accessTokenFactory" src/ -r --include="*.ts" | \
  grep -v "await\|async\|getToken\|refresh"
```

**修正**：
```typescript
// ❌ 错误：静态 Token
.withUrl(hubUrl, {
  accessTokenFactory: () => localStorage.getItem('token'),
})

// ✅ 正确：动态获取 Token
.withUrl(hubUrl, {
  accessTokenFactory: async () => {
    const token = await getAccessToken();  // 可能触发刷新
    return token;
  },
})
```

---

### 反模式 2.4: 无限重连

**问题**：断线重连没有上限，可能导致服务器压力过大。

**检测**：
```bash
# 检测重连逻辑是否有上限检查
grep -A20 "reconnect\|handleDisconnect" src/ -r --include="*.ts" | \
  grep -v "maxReconnect\|reconnectAttempts\|>="
```

**修正**：
```typescript
// ❌ 错误：无限重连
private async handleDisconnect() {
  await this.connection?.start();  // 失败会一直重试
}

// ✅ 正确：有上限的重连
private async handleDisconnect() {
  if (this.reconnectAttempts >= this.maxReconnectAttempts) {
    console.error('Max reconnect attempts reached');
    this.notifyConnectionLost();
    return;
  }
  this.reconnectAttempts++;
  // ... 重连逻辑
}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 连接管理

```typescript
import * as signalR from '@microsoft/signalr';

class SignalRService {
  private connection: signalR.HubConnection | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  async connect(hubUrl: string, accessToken: string) {
    this.connection = new signalR.HubConnectionBuilder()
      .withUrl(hubUrl, {
        accessTokenFactory: async () => await getAccessToken(),
        transport: signalR.HttpTransportType.WebSockets,
      })
      .withAutomaticReconnect({
        nextRetryDelayInMilliseconds: (retryContext) => {
          // 指数退避: 1s, 2s, 4s, 8s, 16s
          return Math.min(1000 * Math.pow(2, retryContext.previousRetryCount), 16000);
        },
      })
      .configureLogging(signalR.LogLevel.Information)
      .build();

    this.setupEventHandlers();
    await this.connection.start();
  }

  private setupEventHandlers() {
    if (!this.connection) return;

    this.connection.onclose((error) => {
      console.log('SignalR disconnected', error);
      this.handleDisconnect();
    });

    this.connection.onreconnecting((error) => {
      console.log('SignalR reconnecting...', error);
    });

    this.connection.onreconnected((connectionId) => {
      console.log('SignalR reconnected', connectionId);
      this.reconnectAttempts = 0;
    });
  }
}
```

### 3.2 流式文本 Hook

```typescript
function useStreamingText(messageId: string) {
  const [text, setText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    const handleChunk = (chunk: string, id: string) => {
      if (id === messageId) {
        setText(prev => prev + chunk);
        setIsStreaming(true);
      }
    };

    const handleComplete = (id: string) => {
      if (id === messageId) {
        setIsStreaming(false);
      }
    };

    connection.on('StreamingMessage', handleChunk);
    connection.on('MessageComplete', handleComplete);

    return () => {
      connection.off('StreamingMessage', handleChunk);
      connection.off('MessageComplete', handleComplete);
    };
  }, [messageId]);

  return { text, isStreaming };
}
```

### 3.3 消息队列（可靠性）

```typescript
class MessageQueue {
  private queue: QueuedMessage[] = [];
  private isProcessing = false;
  private maxRetries = 3;

  enqueue(message: QueuedMessage) {
    this.queue.push(message);
    this.process();
  }

  private async process() {
    if (this.isProcessing || this.queue.length === 0) return;
    this.isProcessing = true;

    while (this.queue.length > 0) {
      const message = this.queue[0];
      try {
        await this.send(message);
        this.queue.shift();
      } catch (error) {
        message.retries++;
        if (message.retries >= this.maxRetries) {
          this.queue.shift();
          this.notifyFailed(message);
        } else {
          await new Promise(r => setTimeout(r, 1000 * message.retries));
        }
      }
    }

    this.isProcessing = false;
  }
}
```

### 3.4 连接状态管理

```typescript
enum ConnectionState {
  Disconnected = 'disconnected',
  Connecting = 'connecting',
  Connected = 'connected',
  Reconnecting = 'reconnecting',
}

function useConnectionState() {
  const [state, setState] = useState<ConnectionState>(
    ConnectionState.Disconnected
  );

  useEffect(() => {
    const updateState = () => {
      switch (connection.state) {
        case signalR.HubConnectionState.Connected:
          setState(ConnectionState.Connected);
          break;
        case signalR.HubConnectionState.Connecting:
          setState(ConnectionState.Connecting);
          break;
        case signalR.HubConnectionState.Reconnecting:
          setState(ConnectionState.Reconnecting);
          break;
        default:
          setState(ConnectionState.Disconnected);
      }
    };

    connection.onreconnecting(() => setState(ConnectionState.Reconnecting));
    connection.onreconnected(() => setState(ConnectionState.Connected));
    connection.onclose(() => setState(ConnectionState.Disconnected));

    updateState();

    return () => {
      // 清理（如果需要）
    };
  }, []);

  return state;
}
```

---

## 4. 自我验证 (Self-Verification)

### SignalR 合规审计脚本

```bash
#!/bin/bash
# signalr-audit.sh - SignalR 代码合规检查

echo "📡 SignalR 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测事件监听清理
echo -e "\n🔌 检测事件监听清理..."
ON_COUNT=$(grep -rn "connection\.on(" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
OFF_COUNT=$(grep -rn "connection\.off(" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

if [ "$ON_COUNT" -gt "$OFF_COUNT" ]; then
    echo "❌ on() 调用 ($ON_COUNT) 多于 off() 调用 ($OFF_COUNT)"
    echo "   可能存在未清理的事件监听"
    ((ERRORS++))
else
    echo "✅ 事件监听清理正常 (on: $ON_COUNT, off: $OFF_COUNT)"
fi

# 2. 检测 invoke 前状态检查
echo -e "\n📤 检测 invoke 状态检查..."
UNSAFE_INVOKE=$(grep -B3 "\.invoke(" src/ -r --include="*.ts" 2>/dev/null | \
  grep -v "state\|Connected\|//" | grep "invoke" | head -5)

if [ -n "$UNSAFE_INVOKE" ]; then
    echo "❌ 发现可能未检查状态的 invoke:"
    echo "$UNSAFE_INVOKE"
    ((ERRORS++))
else
    echo "✅ invoke 调用前有状态检查"
fi

# 3. 检测断线处理
echo -e "\n🔄 检测断线处理..."
ONCLOSE=$(grep -rn "\.onclose(" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$ONCLOSE" -eq 0 ]; then
    echo "❌ 未发现 onclose 处理器"
    ((ERRORS++))
else
    echo "✅ 已配置断线处理 ($ONCLOSE 处)"
fi

# 4. 检测重连上限
echo -e "\n🔁 检测重连上限..."
MAX_RECONNECT=$(grep -rn "maxReconnect\|MAX_RETRY" src/ --include="*.ts" 2>/dev/null | wc -l | tr -d ' ')

if [ "$MAX_RECONNECT" -eq 0 ]; then
    echo "⚠️ 未发现重连上限配置"
else
    echo "✅ 已配置重连上限"
fi

# 5. 检测 Token 动态获取
echo -e "\n🔑 检测 Token 配置..."
STATIC_TOKEN=$(grep -A3 "accessTokenFactory" src/ -r --include="*.ts" 2>/dev/null | \
  grep "localStorage\|sessionStorage" | head -3)

if [ -n "$STATIC_TOKEN" ]; then
    echo "⚠️ Token 可能是静态获取:"
    echo "$STATIC_TOKEN"
else
    echo "✅ Token 配置正常"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ SignalR 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 所有 `connection.on()` 都有对应的 `connection.off()`
- [ ] `invoke()` 前检查 `connection.state === Connected`
- [ ] `accessTokenFactory` 返回 Promise（支持刷新）
- [ ] 配置了 `onclose` 处理断线
- [ ] 重连有最大次数限制
- [ ] 流式消息有 `MessageComplete` 标记

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `zustand-patterns` | 连接状态存储在 Zustand store |
| `react-query-patterns` | 实时数据触发缓存失效 |
| `code-quality-gates` | 检查事件监听清理、错误处理 |

### 关联文件

- `src/features/moss-chat-signalr/**/*.ts`
- `src/hooks/useSignalR*.ts`

---

**✅ SignalR Patterns v2.0.0** | **标准 4 Section 已集成**
