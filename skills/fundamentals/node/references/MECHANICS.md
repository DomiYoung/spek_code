# Node 底层原理扩展

## 事件循环阶段
- timers → pending callbacks → idle/prepare → poll → check → close callbacks。
- 微任务：`process.nextTick` 高于 Promise 微任务。

## libuv 线程池
- fs/crypto/dns 等在 libuv 线程池执行，默认 4 线程。
- 线程池饥饿会放大延迟抖动。

## Streams 与背压
- 关注 `highWaterMark`、`pause/resume` 与 `pipeline`。
- 处理写入返回值与 `drain` 事件避免堆积。

## 模块系统
- CJS/ESM 解析与缓存不同，路径解析影响启动与一致性。

## 诊断工具
- `--inspect` + heap snapshot
- `perf_hooks.monitorEventLoopDelay()`
- `--trace-gc`/`--trace-event-categories=v8`
