---
name: fundamentals-dotnet
description: |
  .NET 底层原理诊断 - CLR/GC/JIT/线程池/异步模型。
  Use when:
  - 内存上涨、GC 停顿
  - 高 CPU/线程池饥饿/异步死锁
  - 性能抖动、冷启动慢
  触发词：.NET、CLR、GC、JIT、IL、Assembly、ThreadPool、async/await、deadlock
  Related Skills: experts/backend, fundamentals/unix, fundamentals/network
allowed-tools: "*"
---

# .NET Fundamentals（CLR 底层原理）

> **目标**：把性能/稳定性问题定位到 CLR、GC、JIT 或线程池层。

## 诊断路径
1. 明确运行时版本与部署模式（框架依赖/自包含）。
2. 判断瓶颈：CPU/内存/线程池/锁竞争。
3. 验证分配与 GC 行为（LOH/Gen0-2/暂停）。
4. 识别同步阻塞与 async 误用。

## 症状 → 机制速查
- **CPU 高但吞吐低** → 线程池饥饿或锁竞争
- **内存持续上涨** → 对象存活期过长或 LOH 膨胀
- **偶发卡顿** → GC 暂停或大量分配
- **异步死锁** → sync-over-async / 上下文捕获
- **冷启动慢** → JIT 预热与程序集加载开销

## 关键机制速记
- **GC 分代**：Gen0/1/2 + LOH，暂停与分配相关
- **线程池**：I/O 与 CPU 线程动态扩缩
- **JIT**：首次调用编译，冷启动成本高
- **同步上下文**：UI/ASP.NET 环境易出现 deadlock

## 证据采集要点
- `dotnet --info` 确认运行时与目标框架
- `dotnet-counters` 观察 GC/线程池/CPU
- `dotnet-trace` 定位热点调用
- 可选：运行 `scripts/diagnose.sh` 输出运行时信息与诊断命令

## 常见根因清单
- sync-over-async（`.Result`/`.Wait()`）导致死锁
- 频繁大对象分配触发 LOH 压力
- 线程池饥饿导致请求排队
- 过度装箱/字符串拼接引发分配暴增
- 冷启动未预热导致首请求延迟

## 快速验证
- 观察 GC 暂停时间与分配速率
- 检查线程池队列长度与吞吐变化

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：GC/JIT/线程池/异步上下文细节
