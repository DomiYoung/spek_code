# 决策树 3: 模式标志 (Mode Flag Router)

**目的**: 决定 SuperClaude 模式和 MCP 标志

## 决策流程图

```
START: 识别任务特征
│
├─ 需要【当前信息/网络搜索/最新版本】？
│   └─ YES → --research
│            启用 Tavily + 深度搜索
│
├─ 涉及【多组件/架构级/跨模块依赖】？
│   └─ YES → --think-hard 或 --ultrathink
│            启用 Sequential + 深度分析
│
├─ 需要【浏览器调试/DevTools/实际渲染】？
│   └─ YES → --chrome 或 --play
│            启用 Playwright/Chrome DevTools
│
├─ 需要【官方文档/库 API/框架模式】？
│   └─ YES → --c7
│            启用 Context7
│
├─ 需要【批量代码变换/模式替换】？
│   └─ YES → --morph
│            启用 Morphllm
│
└─ 默认
    └─ → 无额外标志
         使用标准模式
```

## 标志组合速查

| 场景 | 推荐标志组合 |
|------|-------------|
| 复杂 Bug 调试 | `--chrome --think-hard` |
| 新功能开发 | `--c7 --think` |
| 架构分析 | `--think-hard` |
| 性能优化 | `--chrome --performance` |
| 批量重构 | `--morph` |
| 深度研究 | `--research --think-hard` |

## 标志优先级

1. `--safe-mode` > `--validate` > 其他优化标志
2. 显式用户标志 > 自动检测
3. `--ultrathink` > `--think-hard` > `--think`
4. `--no-mcp` 会覆盖所有单独 MCP 标志
