---
name: fundamentals-typescript
description: |
  TypeScript 底层原理诊断 - 类型系统、结构类型、类型推断、编译流程。
  Use when:
  - 类型推断异常、联合类型收窄失败
  - 泛型推断/约束问题
  - tsconfig/模块解析导致的类型差异
  - 编译产物与运行时不一致
  触发词：TypeScript、tsconfig、类型推断、泛型、结构类型、声明合并、类型收窄、d.ts
  Related Skills: fundamentals/javascript, experts/frontend, experts/backend
allowed-tools: "*"
---

# TypeScript Fundamentals（TS 底层原理）

> **目标**：用类型系统与编译机制解释问题根因，而不是只改类型断言。

## 诊断路径
1. 提炼最小复现（剔除业务噪音）。
2. 确认 `tsconfig` 关键项（`strict`/`target`/`moduleResolution`/`paths`）。
3. 验证类型推断与收窄路径（结构类型、联合类型、泛型约束）。
4. 若与运行时不一致，检查 emit 产物与编译边界。

## 症状 → 机制速查
- **类型变成 any/unknown** → 类型被宽化或跳过检查（结构类型兼容）
- **收窄失败** → 缺少可判别字段或控制流未覆盖
- **类型不匹配却能通过** → 结构类型系统允许兼容
- **声明冲突/污染** → declaration merging 或全局类型扩展
- **运行时崩溃但类型通过** → 类型与真实数据源不一致

## 关键机制速记
- **结构类型**：只看形状，不看名义
- **控制流分析**：分支覆盖决定收窄效果
- **字面量宽化**：未加 const 会扩大类型
- **模块解析**：`moduleResolution`/`paths` 决定类型来源

## 证据采集要点
- `tsc --noEmit` 确认实际诊断
- `tsc --showConfig` 核对编译配置
- `tsc --traceResolution` 排查模块解析
- 可选：运行 `scripts/diagnose.sh` 输出编译器版本与配置提示

## 常见根因清单
- 缺少判别字段导致联合类型无法收窄
- `any`/第三方 `d.ts` 污染全局类型
- `paths`/`baseUrl` 配置导致类型引用错位
- `esModuleInterop`/`moduleResolution` 不一致
- 运行时数据未校验导致“类型通过但值不对”

## 快速验证
- 生成最小复现并单独 `tsc --noEmit`
- 对比 `tsc --showConfig` 与预期配置

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：结构类型、收窄、模块解析与声明合并
