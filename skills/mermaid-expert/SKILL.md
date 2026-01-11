---
name: mermaid-expert
description: |
  Mermaid.js 图表语法专家 - 流程图、时序图、类图等。
  Use when:
  - 画流程图、时序图、类图、状态图、甘特图
  - 生成 Mermaid 代码
  - 在文档中嵌入图表
  触发词：Mermaid、流程图、时序图、类图、diagram、画图、架构图
  Related Skills: obsidian-markdown, json-canvas, experts/architect
allowed-tools: Read, Write, Edit
---

# Mermaid.js 图表语法专家

## 🔍 自动错误诊断规则

> **当用户提供 Mermaid 代码时，自动扫描以下错误模式：**

### 诊断清单（按优先级）

1. **检测 `flowchart` vs `graph`**
   - 错误信号：`Parse error` + `flowchart`
   - 原因：9.x 不完全支持 `flowchart` 关键字
   - 修复：替换为 `graph`

2. **检测 `direction` 指令**
   - 错误信号：`Expecting 'SEMI', 'NEWLINE', 'EOF'` + `direction`
   - 原因：9.x 子图不支持 `direction LR/TB`
   - 修复：删除 `direction` 行

3. **检测 `<br/>` 换行标签**
   - 错误信号：渲染失败或显示原始 HTML
   - 原因：10.x+ 不再支持 `<br/>` 标签
   - 修复：移除 `<br/>` 或用空格替代

4. **检测 Emoji 在 subgraph 标签**
   - 错误信号：`Parse error` + 包含 Emoji 的行
   - 原因：特殊字符需要引号包裹
   - 修复：`subgraph 🔥标题` → `subgraph "🔥标题"`

5. **检测节点 ID 冲突**
   - 错误信号：图表部分渲染或节点丢失
   - 原因：相同 ID 定义多次
   - 修复：使用唯一 ID

6. **检测箭头语法错误**
   - 错误信号：`Parse error` + `-->`
   - 原因：箭头前后缺少空格或节点
   - 修复：确保 `A --> B` 格式正确

7. **检测 class 语句位置错误**
   - 错误信号：`Parse error` + `class "xxx"`
   - 原因：class 语句不能在 subgraph 内部
   - 修复：将所有 class 语句移到文件底部

8. **检测 class 语句逗号后空格**
   - 错误信号：`Expecting... got 'SPACE'`
   - 原因：`class A, B style` 逗号后有空格
   - 修复：移除逗号后的空格 `class A,B style`

### 诊断输出模板

```
🔍 Mermaid 诊断结果：
━━━━━━━━━━━━━━━━━━━━━━
❌ 发现问题：[问题描述]
📍 位置：第 X 行
🔧 修复建议：[具体修复]

✅ 修复后代码：
[修复后的代码]
```

---

## ⚠️ 版本兼容性（9.x → 11.x）

> **关键提醒**：项目可能使用 Mermaid 9.x（如 `"mermaid": "^9.1.6"`），而 LLM 默认生成 10.x+ 语法。必须注意版本差异！

### 版本检测

```typescript
// 在渲染前检测版本
import mermaid from 'mermaid';
const version = mermaid.version;  // "9.1.6" 或 "11.0.0"
const majorVersion = parseInt(version.split('.')[0]);
```

### 语法差异对照表

| 特性 | 9.x 语法 | 10.x+ 语法 | 兼容策略 |
|------|----------|-----------|---------|
| 流程图声明 | `graph TD` | `flowchart TD`（推荐） | 两者都支持，用 `graph` 更安全 |
| 子图方向 | ❌ 不支持 | `direction LR` | 9.x 只能用子图嵌套实现 |
| HTML 换行 | `<br/>` ✅ | ❌ **不支持** | 用 `\n` 或移除换行 |
| 节点文本换行 | 手动换行 | 自动换行 | 用 `<br>` 在 9.x，移除在 10.x+ |
| Emoji | 部分支持 | 完全支持 | 9.x 需要用 Unicode 转义 |
| 类名前缀 | `style` 关键字 | `classDef` 类定义 | 两者都支持 |

### 🔥 常见 LLM 生成的不兼容语法

```mermaid
%% ❌ 10.x+ 语法（9.x 会报错）
flowchart TD
    subgraph 用户层
        direction LR
        A[用户<br/>界面] --> B[API]
    end

%% ✅ 9.x 兼容语法
graph TD
    subgraph 用户层
        A[用户界面] --> B[API]
    end
```

### 自动修复规则

在渲染前应用以下修复：

```typescript
// mermaidFixRules.ts
export function fixMermaidForV9(code: string): string {
  let fixed = code;

  // 1. flowchart -> graph (兼容 9.x)
  fixed = fixed.replace(/^flowchart\s+(TD|TB|LR|RL|BT)/gm, 'graph $1');

  // 2. 移除 direction 指令（9.x 不支持）
  fixed = fixed.replace(/^\s*direction\s+(TB|TD|BT|LR|RL)\s*$/gm, '');

  // 3. 移除 <br/> 和 <br> 换行标签
  fixed = fixed.replace(/<br\s*\/?>/gi, ' ');

  // 4. 处理 Emoji（转义特殊字符）
  fixed = fixed.replace(/subgraph\s+([🇺🇸🇨🇳🔥✅❌🎯📊].+)/gm, (match, label) => {
    return `subgraph "${label}"`;
  });

  return fixed;
}
```

### 版本策略选择

| 策略 | 适用场景 | 实现方式 |
|------|---------|---------|
| **降级兼容** | 项目锁定 9.x | 应用修复规则 + 使用 `graph` 语法 |
| **升级到最新** | 新项目 | 使用 `flowchart` + `direction` |
| **远程渲染** | 两者都要支持 | 使用 mermaid.ink 服务端渲染 |

---


## 🎨 图表类型与示例

> 📖 **详见**: [CHART_EXAMPLES.md](./CHART_EXAMPLES.md) - 包含 7 种图表类型的详细语法和项目实战示例

| 图表类型 | 关键字 | 用途 |
|---------|--------|------|
| 流程图 | `graph` | 流程、决策、系统架构 |
| 序列图 | `sequenceDiagram` | 时序交互、API 调用 |
| 类图 | `classDiagram` | 类结构、对象关系 |
| 状态图 | `stateDiagram-v2` | 状态转换、生命周期 |
| ER 图 | `erDiagram` | 数据库设计、实体关系 |
| 甘特图 | `gantt` | 项目计划、时间线 |
| 旅程图 | `journey` | 用户体验、流程分析 |

---

**✅ Mermaid 专家 Skill 已集成** | **自动图表生成已启用**

