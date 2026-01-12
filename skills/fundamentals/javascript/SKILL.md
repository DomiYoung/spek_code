---
name: fundamentals-javascript
description: |
  JavaScript 底层原理诊断 - 作用域/闭包/原型链/this/异步模型。
  Use when:
  - this 绑定/原型链/继承问题
  - 异步顺序、事件循环、Promise 相关
  - 隐式类型转换、TDZ/Hoisting
  - 内存泄漏或闭包导致的状态异常
  触发词：闭包、原型链、this、Promise、微任务、宏任务、Hoisting、TDZ、作用域链
  Related Skills: fundamentals/browser, fundamentals/react
allowed-tools: "*"
---

# JavaScript Fundamentals（JS 底层原理）

> **目标**：用语言机制解释“为什么这样”而不是只给语法层方案。

## 诊断路径
1. 复现并最小化例子（最小可复现）。
2. 确认机制层面：作用域/this/原型链/异步队列/类型转换。
3. 给出可验证推理：输出顺序/调用栈/内存引用。

## 症状 → 机制速查
- **this 指向异常** → 绑定规则被打破（显式/隐式/默认/箭头）
- **状态“变旧”** → 闭包捕获旧值或引用未更新
- **instanceof 失效** → 原型链被断开或跨 realm
- **Promise 顺序异常** → 微任务/宏任务队列顺序误判
- **变量未定义/提升困惑** → Hoisting/TDZ 误解

## 关键规则速记
- **this 绑定优先级**：new > 显式绑定 > 隐式绑定 > 默认绑定；箭头函数继承外层 this。
- **事件循环顺序**：同步栈 → 微任务（Promise/MutationObserver）→ 宏任务（setTimeout）。
- **原型链查找**：对象自身 → prototype → ... → null。
- **闭包内存**：外层作用域变量被引用就不会释放。

## 证据采集要点
- 最小复现输出顺序与调用栈
- 可选：运行 `scripts/diagnose.sh` 生成事件循环顺序示例

## 快速自检
- 是否在回调中丢失了 this（未 bind/未用箭头函数）
- 是否把“值”当成“引用”（对象/数组）
- 是否混用 ESM/CJS 导致默认导出差异

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：this/原型链/事件循环/类型转换
