---
name: fundamentals-unix
description: |
  Unix 底层原理诊断 - 进程/线程/调度/虚拟内存/文件系统/系统调用。
  Use when:
  - 进程/线程异常、CPU 100%、僵尸进程
  - 文件描述符泄漏、权限问题
  - I/O 卡顿、磁盘/缓存异常
  触发词：Unix、Linux、POSIX、fork、exec、signal、fd、系统调用、虚拟内存、文件系统
  Related Skills: fundamentals/macos, fundamentals/network, experts/backend
allowed-tools: "*"
---

# Unix Fundamentals（Unix 底层原理）

> **目标**：从进程、系统调用与文件系统层面解释异常行为。

## 诊断路径
1. 复现并定位进程（`ps`/`top`/`htop`）。
2. 检查文件描述符与资源上限（`lsof`/`ulimit`）。
3. 区分 CPU vs I/O 瓶颈（`iostat`/`vmstat`）。
4. 需要时跟踪系统调用（`strace` 或 macOS 的 `dtruss`）。

## 症状 → 机制速查
- **CPU 100%** → 忙等待/系统调用频繁/上下文切换过多
- **僵尸进程** → 父进程未 `wait` 回收
- **too many open files** → fd 泄漏或上限过低
- **权限拒绝** → UID/GID/ACL 或挂载参数限制
- **I/O 卡顿** → 页缓存不足或同步写阻塞

## 关键机制速记
- **进程状态**：R/S/D/Z 反映调度与阻塞原因
- **文件描述符**：进程级资源，需显式关闭
- **页缓存**：I/O 与内存交互层，影响读写延迟
- **系统调用**：阻塞点通常出现在读写/锁等待

## 证据采集要点
- 进程状态、打开文件数、系统负载
- 关键系统调用与阻塞点
- 可选：运行 `scripts/diagnose.sh` 输出系统与进程快照

## 常见根因清单
- 子进程未回收导致僵尸堆积
- fd 泄漏触发资源耗尽
- 长时间同步 I/O 阻塞主线程
- 权限/挂载参数导致访问被拒
- 频繁 fork/exec 造成系统开销

## 快速验证
- `ps -o stat,ppid,pid,comm -p <pid>`
- `lsof -p <pid> | wc -l`
- `ulimit -n` 与配置上限对比

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：进程调度、fd、虚拟内存与系统调用
