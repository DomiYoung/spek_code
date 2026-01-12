---
name: skill-composer
description: |
  技能组合器 - 识别任务需要的多个 Skills 并协同调用。
  Use when:
  - 任务涉及多个技术领域（如 Obsidian + 流程图）
  - 需要多专家视角分析问题
  - 用户问"有哪些相关的 Skill"
  触发词：相关的、还有哪些、一起用、组合、多个
---

# Skill Composer（技能组合器）

> **核心理念**：复杂任务 = 多个 Skills 协同，而非单一 Skill 独立工作。

---

## Skill 调用链证据（强制）

> **目的**：让用户看到实际读取了哪些 Skill，而不是“口头提到”。

### 执行规则
1. **先读后说**：每个激活 Skill 必须先读取 `SKILL.md`。
2. **证据可定位**：每个 Skill 至少给出 1 条证据锚点（标题/小节/反模式名）。
3. **多 Skill 必须列全**：主/辅所有 Skill 都要出现在证据卡片中。
4. **不得伪造**：未读取则标记 `MISSING` 并说明原因。

### 证据卡片格式（固定）

```
╔═══════════════════════════════════════════════════════╗
║  🔍 SKILL 调用链（证据）                               ║
╠═══════════════════════════════════════════════════════╣
║  任务: [一句话描述]                                     ║
║  组合 Skill: skill-a ✅ 已读取                          ║
║              skill-b ✅ 已读取                         ║
║  读取证据:                                            ║
║   - skills/skill-a/SKILL.md → 关键规则/反模式标题        ║
║   - skills/skill-b/references/xxx.md → 关键机制小节      ║
╚═══════════════════════════════════════════════════════╝
```

## Skill 分组索引

### 📝 Obsidian 生态
| Skill | 用途 | 文件类型 |
|-------|------|---------|
| obsidian-markdown | Markdown 笔记、wikilinks、callouts | .md |
| obsidian-bases | 数据库视图、过滤器、公式 | .base |
| json-canvas | 可视化画布、节点连线 | .canvas |

### 📊 可视化/图表
| Skill | 用途 |
|-------|------|
| mermaid-expert | 流程图、时序图、类图 |
| echarts-patterns | 数据可视化图表 |
| reactflow-patterns | 交互式工作流编辑器 |

### 📄 文档生成
| Skill | 用途 | 文件类型 |
|-------|------|---------|
| docx | Word 文档生成 | .docx |
| pptx | PPT 演示文稿 | .pptx |
| xlsx | Excel 电子表格 | .xlsx |
| pdf | PDF 表单填充 | .pdf |

### ⚛️ React 生态
| Skill | 用途 |
|-------|------|
| reactflow-patterns | 节点/边/画布 |
| zustand-patterns | 状态管理 |
| react-query-patterns | 数据请求/缓存 |
| react-hook-form-patterns | 表单验证 |
| react-router-patterns | 路由 |

### 🎨 UI 组件
| Skill | 用途 |
|-------|------|
| shadcn-ui-patterns | Shadcn/Radix 组件 |
| tailwindcss-patterns | Tailwind CSS |
| framer-motion-patterns | 动画 |
| antd-patterns | Ant Design |

### 🔌 后端/通信
| Skill | 用途 |
|-------|------|
| signalr-patterns | 实时通信/WebSocket |
| postgresql-design | 数据库设计 |
| oidc-auth-patterns | 认证/授权 |
| indexeddb-patterns | 离线存储 |

### 🧠 专家系统
| Skill | 用途 |
|-------|------|
| experts/architect | 系统架构设计 |
| experts/performance | 性能优化 |
| experts/frontend | 前端最佳实践 |
| experts/backend | 后端最佳实践 |
| experts/database | 数据库专家 |

### 🧱 底层原理
| Skill | 用途 |
|-------|------|
| fundamentals/browser | 浏览器事件循环/渲染/内存 |
| fundamentals/javascript | JS 作用域/闭包/原型链 |
| fundamentals/network | DNS/TCP/TLS/HTTP/缓存 |
| fundamentals/css | 层叠/BFC/布局/渲染 |
| fundamentals/react | Fiber/调度/Hooks |
| fundamentals/typescript | 类型系统/推断/编译 |
| fundamentals/dotnet | CLR/GC/JIT/线程池 |
| fundamentals/unix | 进程/系统调用/文件系统 |
| fundamentals/macos | XNU/权限/签名 |
| fundamentals/database | SQL/执行计划/事务 |
| fundamentals/python | 解释器/GIL/字节码 |
| fundamentals/node | libuv/事件循环/背压 |
| fundamentals/vue | 响应式/渲染/调度 |
| fundamentals/chrome | 多进程/Blink/GPU |

### 📋 工作流
| Skill | 用途 |
|-------|------|
| workflow-orchestrator | 任务编排/权重评估 |
| planning-with-files | 文件持久化规划 |
| brainstorm | 脑暴/多方案对比 |
| speckit.* | Spec-Kit 系列（9个） |

---

## 组合模式

### 模式 1: Sequential Chain（串行链）

```
任务: 设计并实现用户认证
    │
    ├── speckit.specify（写规范）
    │         ↓
    ├── experts/architect（架构设计）
    │         ↓
    ├── oidc-auth-patterns（认证实现）
    │         ↓
    └── code-quality-gates（代码审查）
```

### 模式 2: Parallel Ensemble（并行集成）

```
任务: 分析这个组件的问题
    │
    ├── experts/performance（性能视角）
    ├── experts/frontend（代码质量视角）
    └── zustand-patterns（状态管理视角）
    │
    └── 综合分析结果
```

### 模式 3: Domain Cluster（领域聚类）

```
任务: 写 Obsidian 工作流文档
    │
    └── Obsidian Cluster:
        ├── obsidian-markdown（文档内容）
        ├── json-canvas（画布布局）
        └── mermaid-expert（流程图）
```

---

## 常见组合

| 场景 | 触发的 Skills |
|------|--------------|
| 写 Obsidian 笔记+图表 | obsidian-markdown + mermaid-expert |
| 画 Obsidian 画布 | json-canvas + mermaid-expert |
| 实现工作流编辑器 | reactflow-patterns + zustand-patterns |
| 创建数据看板 | echarts-patterns + react-query-patterns |
| 设计 API | experts/architect + postgresql-design + oidc-auth-patterns |
| 性能优化 | experts/performance + react-query-patterns + virtual-list-patterns |
| 生成报告 | docx + mermaid-expert + echarts-patterns |

---

## 使用方法

当识别到任务涉及多个领域时：

1. **列出相关 Skills**：明确告知用户将使用哪些 Skills
2. **按顺序/并行加载**：根据任务需要选择组合模式
3. **输出证据卡片**：列出已读取的 Skill 与证据锚点
4. **综合输出**：整合多个 Skills 的指导

**示例输出**：
```
📚 检测到多领域任务，将组合使用以下 Skills：
├── obsidian-markdown（文档结构）
├── json-canvas（画布布局）
└── mermaid-expert（流程图）

开始执行...
```

---

## 1% 原则（增强版）

> **如果有 1% 的可能性某个 Skill 适用，必须调用它。**
> **如果任务涉及多个领域，必须组合调用相关 Skills。**
