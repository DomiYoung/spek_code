---
name: fundamentals-vue
description: |
  Vue 底层原理诊断 - 响应式系统、渲染与调度、编译与运行时。
  Use when:
  - 响应式不更新/更新异常
  - render 频繁/性能抖动
  - watch/computed 行为异常
  - SSR hydration 不一致
  触发词：Vue、reactivity、ref、reactive、computed、watch、nextTick、patch、hydration
  Related Skills: experts/frontend, fundamentals/javascript
allowed-tools: "*"
---

# Vue Fundamentals（Vue 底层原理）

> **目标**：定位到响应式依赖追踪与渲染调度机制。

## 诊断路径
1. 明确版本（Vue2/3）与运行模式（SSR/CSR）。
2. 检查依赖收集与触发链路（effect/track/trigger）。
3. 观察渲染批处理与调度（scheduler/nextTick）。
4. SSR 关注 hydration 差异来源。

## 症状 → 机制速查
- **状态不更新** → 依赖未追踪或解构丢失响应性
- **重复渲染** → 依赖过度或副作用引发回环
- **computed 不生效** → 缺少依赖或缓存失效
- **Hydration mismatch** → 服务端/客户端渲染输出不一致

## 证据采集要点
- Vue DevTools 观察依赖与渲染次数
- 检查响应式 API 使用方式

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：依赖追踪、调度队列、computed 缓存与 SSR
