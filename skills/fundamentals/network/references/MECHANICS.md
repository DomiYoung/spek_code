# 网络机制扩展

## 请求阶段
- DNS → TCP → TLS → TTFB → 下载。
- 建立连接成本决定首包延迟。

## 缓存语义
- Cache-Control/ETag/Last-Modified 影响命中。
- 强缓存优先于协商缓存。

## HTTP/2/3
- 多路复用降低连接数，但仍可能队首阻塞。
- QUIC（HTTP/3）减少握手成本。

## 实时通信
- WebSocket 需要心跳与重连。
- SSE 适合单向流式更新。
