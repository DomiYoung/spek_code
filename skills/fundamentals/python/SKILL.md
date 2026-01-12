---
name: fundamentals-python
description: |
  Python 底层原理诊断 - CPython/GIL/字节码/内存管理/asyncio。
  Use when:
  - 性能慢、CPU 占用高、线程无效
  - 内存增长/泄漏、对象无法释放
  - asyncio/协程时序异常
  - 导入/运行时行为与预期不一致
  触发词：Python、CPython、GIL、字节码、引用计数、GC、asyncio、协程、解释器
  Related Skills: fundamentals/unix, fundamentals/network, experts/backend
allowed-tools: "*"
---

# Python Fundamentals（Python 底层原理）

> **目标**：从解释器/GIL/内存模型定位性能与行为异常。

## 诊断路径
1. 明确解释器与版本（CPython/PyPy/版本号）。
2. 判断瓶颈：CPU 绑定、I/O 绑定、锁竞争。
3. 检查对象生命周期：引用计数/循环引用/GC。
4. 异步问题定位到事件循环与任务调度。

## 症状 → 机制速查
- **多线程无加速** → GIL 限制 CPU 并行
- **内存持续上涨** → 引用未释放或循环引用
- **协程卡住/顺序异常** → 事件循环阻塞或 await 链断裂
- **导入行为异常** → 模块缓存与路径解析

## 证据采集要点
- `python -VV` 确认解释器与编译信息
- `PYTHONTRACEMALLOC`/`tracemalloc` 追踪分配
- `asyncio.get_running_loop()`/任务列表定位阻塞

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：GIL、字节码执行、内存与 GC、asyncio 调度
