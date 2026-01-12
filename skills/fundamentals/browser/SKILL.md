---
name: fundamentals-browser
description: |
  浏览器底层原理诊断 - 事件循环、渲染流水线、V8/内存、安全模型。
  Use when:
  - 页面卡顿、白屏、渲染异常、布局错乱
  - 输入延迟、动画掉帧、长任务
  - 内存泄漏、页面崩溃
  - CORS/CSP/跨域相关问题
  触发词：事件循环、渲染、重排、重绘、合成层、V8、GC、内存、CORS、CSP
  Related Skills: experts/performance, experts/frontend, fundamentals/javascript, fundamentals/css, fundamentals/network
allowed-tools: "*"
---

# Browser Fundamentals（浏览器底层原理）

> **目标**：用“机制 → 证据 → 修复”的方式解释浏览器问题，而不是只给技巧。

## 诊断路径（强制顺序）
1. 复现问题并记录环境（设备/浏览器/版本/网络/是否扩展）。
2. 判断瓶颈层级：Main Thread、Rendering、GPU、Network、Memory。
3. 采集证据：Performance、Memory、Network、Console。
4. 映射到机制 → 提出修复 → 验证效果。

## 症状 → 机制速查
- **输入延迟/卡顿** → 事件循环被长任务阻塞（>50ms）
- **动画掉帧/滚动抖动** → 布局/绘制过重或频繁重排
- **布局跳动（CLS）** → 关键资源后到或尺寸未预留
- **白屏/渲染不出** → 渲染被阻塞（CSS/JS/字体）
- **内存持续上涨** → DOM/事件监听/闭包未释放
- **跨域报错** → CORS/CSP/同源策略

## 证据采集要点
- **Performance**：Main Thread 长任务、布局/绘制占比、强制同步布局（Layout）
- **Rendering**：FPS、Paint flashing、Layer borders
- **Memory**：Heap snapshot 对比、Detached DOM tree
- **Network**：关键资源瀑布图、阻塞请求、TTFB
- **Console**：CORS/CSP/Mixed Content
- 可选：运行 `scripts/diagnose.sh` 输出系统信息与检查提示

## 常见根因清单
- 读写布局交错导致强制同步布局（Layout Thrashing）
- 频繁触发重排/重绘，合成层不合理
- 大量 DOM 节点/大图片/未压缩资源
- 事件监听/定时器未清理导致内存泄漏
- 阻塞式脚本或大量同步计算

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：渲染流水线、事件循环、内存与安全模型
