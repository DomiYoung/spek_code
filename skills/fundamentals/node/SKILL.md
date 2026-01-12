---
name: fundamentals-node
description: |
  Node.js 底层原理诊断 - 事件循环/libuv/V8/模块系统/流与背压。
  Use when:
  - 事件循环阻塞、延迟抖动
  - 内存泄漏、GC 频繁
  - Stream 背压/吞吐异常
  - 模块解析/运行时差异
  触发词：Node、Node.js、libuv、Node 事件循环、worker_threads、stream、背压、perf_hooks
  Related Skills: fundamentals/javascript, fundamentals/unix, fundamentals/network
allowed-tools: "*"
---

# Node Fundamentals（Node 底层原理）

> **目标**：将问题定位到事件循环、libuv 或 V8 层。

## 诊断路径
1. 区分 CPU 绑定 vs I/O 绑定。
2. 查看事件循环延迟与长任务。
3. 检查内存与 GC 行为。
4. 对流/队列问题确认背压链路。

## 症状 → 机制速查
- **请求延迟抖动** → 事件循环阻塞或任务堆积
- **CPU 高但吞吐低** → 同步计算堵塞主线程
- **内存上涨** → 闭包/缓存/监听器未释放
- **Stream 卡顿** → 背压未处理或高水位设置不当

## 证据采集要点
- `node --trace-gc`/`--trace-event-categories=v8` 观察 GC
- `perf_hooks.monitorEventLoopDelay()` 监测事件循环
- `--inspect` + heap snapshot 查泄漏

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：事件循环阶段、libuv 线程池、背压与模块解析
