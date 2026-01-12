---
name: fundamentals-css
description: |
  CSS 底层原理诊断 - 层叠/特异性/BFC/布局/重排重绘。
  Use when:
  - 样式不生效、优先级混乱
  - 布局错位、z-index 无效
  - 动画掉帧、滚动卡顿
  触发词：层叠、特异性、BFC、z-index、stacking context、盒模型、选择器
  Related Skills: fundamentals/browser, experts/frontend
allowed-tools: "*"
---

# CSS Fundamentals（CSS 底层原理）

> **目标**：把“样式不对”定位到层叠、布局或渲染阶段。

## 诊断路径
1. 确认选择器是否命中（DevTools 看规则）。
2. 判断优先级来源（特异性/顺序/important）。
3. 若是性能问题，区分 reflow / repaint / composite。

## 症状 → 机制速查
- **样式不生效** → 选择器未命中或被更高特异性覆盖
- **z-index 无效** → 新的 stacking context 或定位缺失
- **布局错位** → BFC/包含块/盒模型计算偏差
- **滚动卡顿** → 频繁 reflow 或大量 paint
- **动画掉帧** → 触发 layout/paint 而非合成层

## 关键机制速记
- **特异性**：inline > id > class/属性 > 元素
- **BFC**：隔离浮动、清除外边距折叠
- **合成层**：transform/opacity 更易走 GPU

## 证据采集要点
- Computed/Matched Rules 确认命中与覆盖来源
- Performance 面板观察 Style/Layout/Paint 占比
- Rendering 面板开启 Paint flashing/Layer borders

## 常见根因清单
- 选择器过于宽泛/过深导致覆盖混乱
- 未建立定位上下文导致 z-index 失效
- 读写布局交错触发强制同步布局
- 动画触发 layout/paint 而非合成层
- 缺少尺寸约束导致 CLS 或布局抖动

## 快速验证
- DevTools 中查看 Computed/Matched CSS
- 开启 Paint flashing、Layer borders

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：层叠规则、BFC、合成与性能陷阱
