# Python 底层原理扩展

## GIL 与并发模型
- GIL 只允许单线程执行字节码，CPU 密集型需多进程或 C 扩展释放 GIL。
- I/O 密集型可用线程/协程提升吞吐。

## 字节码与执行模型
- 源码 → AST → 字节码，解释器执行 frame。
- 动态特性带来运行时开销与类型不一致风险。

## 内存与 GC
- 引用计数为主，循环引用由分代 GC 处理。
- 大量短生命周期对象会放大分配/回收开销。

## asyncio 调度
- 事件循环负责调度任务；阻塞调用会拖慢全局。
- 注意 await 链完整性与取消/超时处理。

## 快速排查清单
- `python -VV`/`sys.implementation` 确认解释器。
- `tracemalloc`/`gc.get_objects()` 观察泄漏。
- `asyncio.all_tasks()` 定位挂起任务。
