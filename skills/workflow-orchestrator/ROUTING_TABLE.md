# Skill 路由表

> **完整覆盖 74 个 Skills**，按领域分类。
> **1% 原则**：如果有 1% 的可能性某个 skill 适用，必须调用它。

---

## 工作流/规划（自动触发）

| 关键词 | 触发 Skill | 触发方式 |
|--------|-----------|---------|
| 每个任务开始 | `workflow-orchestrator` | 自动 |
| 权重 ≥7 | `speckit.constitution` → `speckit.specify` → `speckit.plan` → `speckit.tasks` → `speckit.implement` | 自动串联 |
| 权重 3-6 | `planning-with-files` | 自动 |
| 脑暴、方案对比 | `brainstorm` | 语义检测 |
| 记忆编排 | `mem-orchestrator` | 自动 |
| 记忆规划 | `mem-plan` | 自动 |

## Spec-Kit 系列（权重≥7 自动串联）

| 阶段 | Skill | 说明 |
|------|-------|------|
| 1. 宪法 | `speckit.constitution` | 项目原则 |
| 2. 规范 | `speckit.specify` | 需求规范 |
| 3. 澄清 | `speckit.clarify` | 需求澄清 |
| 4. 规划 | `speckit.plan` | 实现规划 |
| 5. 任务 | `speckit.tasks` | 任务分解 |
| 6. 分析 | `speckit.analyze` | 代码分析 |
| 7. 实现 | `speckit.implement` | 执行实现 |
| 8. 清单 | `speckit.checklist` | 检查清单 |
| 9. Issues | `speckit.taskstoissues` | 转 Issues |

## Task Master 系列

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 下一个任务 | `tm-next` | 任务管理 |
| 完成任务 | `tm-complete` | 任务完成 |
| 显示任务 | `tm-show` | 任务列表 |

## 专家系统

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 专家路由 | `expert-router` | 自动 |
| 前端专家 | `experts/frontend` | 语义匹配 |
| 后端专家 | `experts/backend` | 语义匹配 |
| 架构师 | `experts/architect` | 语义匹配 |
| 数据库专家 | `experts/database` | 语义匹配 |
| 性能专家 | `experts/performance` | 语义匹配 |
| 质量专家 | `experts/quality` | 语义匹配 |
| 产品经理 | `experts/product` | 语义匹配 |

## 底层原理

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 事件循环、渲染、重排、重绘、合成层、V8、GC、CORS、CSP | `fundamentals/browser` | 语义匹配 |
| 闭包、原型链、this、Promise、微任务、宏任务、Hoisting、TDZ、作用域链 | `fundamentals/javascript` | 语义匹配 |
| DNS、TCP、TLS、HTTP2、HTTP3、TTFB、缓存、CDN、WebSocket、SSE | `fundamentals/network` | 语义匹配 |
| 层叠、特异性、BFC、z-index、stacking context、盒模型、选择器、CSS 优先级 | `fundamentals/css` | 语义匹配 |
| React、Fiber、reconciliation、Hooks、useEffect、useLayoutEffect、StrictMode、Concurrent | `fundamentals/react` | 语义匹配 |
| TypeScript、tsconfig、类型推断、泛型、结构类型、声明合并、类型收窄、d.ts | `fundamentals/typescript` | 语义匹配 |
| .NET、CLR、GC、JIT、IL、Assembly、ThreadPool、async/await、deadlock | `fundamentals/dotnet` | 语义匹配 |
| Unix、Linux、POSIX、fork、exec、signal、fd、系统调用、虚拟内存 | `fundamentals/unix` | 语义匹配 |
| macOS、XNU、launchd、SIP、codesign、notarization、sandbox、keychain、entitlements | `fundamentals/macos` | 语义匹配 |
| SQL、索引、执行计划、事务、隔离级别、锁、MVCC、WAL、B-Tree | `fundamentals/database` | 语义匹配 |
| Python、CPython、GIL、字节码、引用计数、GC、asyncio、协程、解释器 | `fundamentals/python` | 语义匹配 |
| Node、Node.js、libuv、Node 事件循环、worker_threads、stream、背压、perf_hooks | `fundamentals/node` | 语义匹配 |
| Vue、reactivity、ref、reactive、computed、watch、nextTick、patch、hydration | `fundamentals/vue` | 语义匹配 |
| Chrome、Chromium、Blink、GPU 进程、渲染进程、Site Isolation、sandbox | `fundamentals/chrome` | 语义匹配 |

## 质量门禁

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 代码质量、lint | `code-quality-gates` | 代码变更后 |
| Spec 验证 | `spec-quality-gates` | Spec 文件检查 |
| 完成审核、提交前 | `review-quality-gates` | 任务完成时 |
| commit、提交代码 | `smart-commit` | Git 操作 |

## 前端开发

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| React、UI、前端、组件 | `frontend-design` | 检查涉及文件路径 |
| shadcn、Radix、headless | `shadcn-ui-patterns` | 检查组件库 |
| Radix UI、Dialog、Dropdown | `radix-ui-patterns` | 检查 Radix 组件 |
| TailwindCSS、utility、className | `tailwindcss-patterns` | 检查样式 |
| 表单、validation、zod | `react-hook-form-patterns` | 检查表单处理 |
| 路由、Router、权限守卫 | `react-router-patterns` | 检查路由配置 |
| 动画、motion、transition | `framer-motion-patterns` | 检查动画效果 |
| 移动端、响应式、rem、vw | `h5-responsive` | 检查移动适配 |

## 状态管理

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| Zustand、Store、全局状态 | `zustand-patterns` | 检查状态管理 |
| React Query、缓存、staleTime | `react-query-patterns` | 检查数据获取 |
| IndexedDB、Dexie、本地存储 | `indexeddb-patterns` | 检查本地缓存 |

## 实时通信

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| SignalR、WebSocket、实时 | `signalr-patterns` | 检查实时通信 |
| OIDC、SSO、Token、认证 | `oidc-auth-patterns` | 检查认证流程 |

## 可视化/图表

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| Mermaid、图表、流程图 | `mermaid-expert` | 检查图表需求 |
| Mermaid 语法、diagram | `mermaid-diagrams` | 检查 Mermaid 代码 |
| ECharts、统计图、饼图 | `echarts-patterns` | 检查数据可视化 |
| ReactFlow、节点、工作流 | `reactflow-patterns` | 检查工作流组件 |
| BPMN、流程建模、审批流 | `bpmn-workflow-patterns` | 检查流程设计 |
| MxGraph、DrawIO | `mxgraph-patterns` | 检查图形编辑 |

## 表格/列表

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| AG-Grid、表格、columnDefs | `ag-grid-patterns` | 检查企业表格 |
| 虚拟列表、virtuoso、滚动 | `virtual-list-patterns` | 检查长列表 |

## 低代码/配置

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 低代码、配置驱动、动态表单 | `lowcode-engine-patterns` | 检查配置化开发 |

## 数据库

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| PostgreSQL、SQL、数据库 | `postgresql-design` | 检查数据库设计 |

## 文档处理

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| Word、docx、文档 | `docx` | 检查文档生成 |
| PDF、表单填充 | `pdf` | 检查 PDF 处理 |
| PPT、pptx、演示 | `pptx` | 检查演示文稿 |
| Excel、xlsx、电子表格 | `xlsx` | 检查表格处理 |
| JSON Canvas、.canvas | `json-canvas` | 检查 Canvas 文件 |
| 微信文章 | `wechat-article-writing` | 检查公众号 |
| X/Twitter 文章 | `x-articles-writing` | 检查推文 |

## 开发工具

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| MCP Server、工具集成 | `mcp-builder` | 检查 MCP 开发 |
| Web Artifact、多组件 | `web-artifacts-builder` | 检查复杂 Artifact |
| Webapp 测试、Playwright | `webapp-testing` | 检查前端测试 |
| 工具高亮、MCP 调用 | `tool-activation-banner` | 检查工具提示 |
| Skill 创建 | `skill-creator` | 检查是否创建 Skill |
| Skills 系统、能力 | `skills-overview` | 检查系统说明 |

## 设计/交互

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 交互设计、HCI、可用性 | `interaction-design-science` | 检查交互体验 |
| Google 规范、Material | `google-dev-quality` | 检查设计规范 |
| AI 开发、Prompt 工程 | `ai-dev-excellence` | 检查 AI 最佳实践 |

## 沟通协作

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 文档共创、协作 | `doc-coauthoring` | 检查文档协作 |
| 内部沟通、状态报告 | `internal-comms` | 检查内部通讯 |

## Obsidian 相关

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| Obsidian Bases | `obsidian-bases` | 检查 Bases 功能 |
| Obsidian Markdown | `obsidian-markdown` | 检查 MD 格式 |

## 复用检查

| 关键词 | 触发 Skill | 确认方式 |
|--------|-----------|---------|
| 组件复用、重复检查 | `patterns/component-reuse` | 开发前检查 |

---

## 路由输出格式

```
╔════════════════════════════════════════════════════════╗
║  🎯 Skill 路由                                          ║
╠════════════════════════════════════════════════════════╣
║  匹配关键词: [xxx]                                      ║
║  触发 Skill: [skill-name]                               ║
║  Skill 路径: skills/[skill-name]/SKILL.md               ║
╚════════════════════════════════════════════════════════╝
```
