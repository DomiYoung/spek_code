---
name: fundamentals-chrome
description: |
  Chrome/Chromium 架构原理诊断 - 多进程模型/Blink/V8/GPU/安全隔离。
  Use when:
  - Chrome 专有渲染/性能问题
  - GPU 进程崩溃或渲染异常
  - Site Isolation/沙箱相关问题
  - 扩展/策略影响行为
  触发词：Chrome、Chromium、Blink、GPU 进程、渲染进程、Browser 进程、Site Isolation、sandbox、Network Service
  Related Skills: fundamentals/browser, fundamentals/network, fundamentals/unix
allowed-tools: "*"
---

# Chrome Fundamentals（Chrome 底层原理）

> **目标**：把问题定位到 Chromium 的进程架构与安全/渲染组件。

## 诊断路径
1. 明确版本与通道（Stable/Beta/Canary）。
2. 判定进程层级：Browser/Renderer/GPU/Network Service。
3. 检查 Site Isolation、沙箱与策略限制。
4. 复现时禁用扩展以排除干扰。

## 症状 → 机制速查
- **渲染异常/白屏** → Renderer 进程崩溃或合成失败
- **GPU 崩溃** → GPU 进程异常或驱动问题
- **跨域异常** → Network Service/隔离策略限制
- **Chrome 特有行为** → Chromium 实现差异

## 证据采集要点
- `chrome://gpu`、`chrome://process-internals`
- `chrome://net-export` 采集网络日志
- `chrome://crashes` 查看崩溃信息

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：多进程架构、Blink 渲染流水线、Site Isolation
