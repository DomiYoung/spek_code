---
name: fundamentals-react
description: |
  React 底层原理诊断 - Fiber、reconciliation、调度与 Hooks 行为。
  Use when:
  - 组件重复渲染/性能问题
  - useEffect/状态更新时序异常
  - 依赖项/闭包导致的 Bug
  - StrictMode 双调用等现象
  触发词：React、Fiber、reconciliation、Hooks、useEffect、useLayoutEffect、StrictMode、Concurrent
  Related Skills: experts/frontend, experts/performance, fundamentals/javascript
allowed-tools: "*"
---

# React Fundamentals（React 底层原理）

> **目标**：把问题定位到 React 的渲染与调度机制。

## 诊断路径
1. 复现并确认运行环境（是否 StrictMode/并发模式）。
2. 区分 render 阶段与 commit 阶段问题。
3. 找到触发渲染的来源（state/props/context）。
4. 用 Profiler 证据说明代价与频率。

## 症状 → 机制速查
- **无意义重渲染** → props 引用不稳定或父组件频繁更新
- **副作用时序异常** → useEffect 运行在 commit 之后
- **状态“变旧”** → 闭包捕获旧 state
- **开发环境双调用** → StrictMode 预期行为
- **UI 卡顿** → 大量渲染或同步计算阻塞
- **依赖异常触发** → Effect 依赖过宽或不稳定引用

## 关键机制速记
- **Fiber**：可中断渲染，调度优先级
- **批量更新**：同一事件循环内 state 会被批处理
- **useLayoutEffect**：commit 前同步执行
- **并发更新**：渲染可被打断，commit 才会生效

## 证据采集要点
- React DevTools Profiler（Commit 次数、耗时、触发源）
- Highlight updates + why-did-you-render（定位无效渲染）
- 检查 props/context 变化轨迹（引用稳定性）

## 常见根因清单
- 父组件每次 render 产生新对象/函数
- Context value 未 memo 导致全量更新
- 列表 key 不稳定导致重建
- useEffect 依赖写法不稳定/缺失
- 重计算放在 render 中

## 快速验证
- React DevTools Profiler 查看渲染次数
- 排查 props 是否稳定（memo/useMemo/useCallback）

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：Fiber/调度/reconciliation/StrictMode
