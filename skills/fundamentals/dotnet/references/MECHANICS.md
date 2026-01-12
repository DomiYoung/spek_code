# .NET 机制扩展

## GC 与 LOH
- Gen0/1/2 + LOH 分代回收，LOH 压力影响停顿。

## 线程池
- 线程池饥饿会降低吞吐并增加延迟。

## JIT
- 首次调用编译造成冷启动开销。

## 同步上下文
- ASP.NET/GUI 上下文容易触发 deadlock。
